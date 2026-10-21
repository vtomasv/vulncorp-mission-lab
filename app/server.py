"""Centro de misión local: persistencia SQLite, evidencia y decisiones auditables."""
import hashlib
import io
import json
import os
import sqlite3
import time
import uuid
import sys
from contextlib import closing
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from .fixtures import CLIENTS,FINDINGS,ASSETS,MISSIONS,CORPUS
from .risk import evaluate,ssvc
from . import ai

ROOT=Path(__file__).resolve().parents[1]
DB=Path(os.environ.get('LAB_DB','/state/mission.db'))
from .secure import secret
CONTROL_KEY=secret('control')

def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB,timeout=10);c.row_factory=sqlite3.Row
    c.execute('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT, created TEXT, body TEXT)')
    return c

def records(kind):
    with closing(connect()) as c:return [json.loads(r['body']) for r in c.execute('SELECT body FROM records WHERE kind=? ORDER BY rowid',(kind,))]

def save(kind,body):
    if kind in ['decision','ai','review','portfolio','triage','control','scan','note','lab_record']:
        runs=records('game_campaign')
        if runs:body={**body,'game_run':runs[-1]['id']}
    item={**body,'id':body.get('id') or kind.upper()+'-'+uuid.uuid4().hex[:10],
          'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    with closing(connect()) as c:
        with c:c.execute('INSERT OR REPLACE INTO records VALUES (?,?,?,?)',(item['id'],kind,item['created_at'],json.dumps(item,ensure_ascii=False)))
    return item

def request_target(url,data=None,headers=None):
    req=Request(url,data=json.dumps(data).encode() if data is not None else None,
                headers={**({'Content-Type':'application/json'} if data is not None else {}),**(headers or {})})
    start=time.monotonic()
    try:
        with urlopen(req,timeout=4) as r:status=r.status;body=json.load(r)
    except HTTPError as e:status=e.code;body=json.load(e)
    except (OSError,ValueError):status=0;body={'error':'Servicio no disponible. Revisa el estado del laboratorio.'}
    return {'status':status,'body':body,'elapsed_ms':round((time.monotonic()-start)*1000)}

def export_bundle():
    bundle={'format':'vulncorp-evidence/1.1','synthetic':True,'legal_submission':False,'exported_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            **{k:records(k) for k in ['evidence','decision','note','ai','review','triage','control','scan','context','portfolio','station','game_campaign','game_activation','game_award','game_analysis']}}
    bundle.update(lab_event=records('lab_event'),lab_record=records('lab_record'))
    canonical=json.dumps(bundle,sort_keys=True,ensure_ascii=False).encode()
    return {**bundle,'content_sha256':hashlib.sha256(canonical).hexdigest()}

def known_evidence():return {d['id'] for d in CORPUS}|{r['id'] for r in records('evidence')}

def nonempty(value,minlength=1,maxlength=4000):
    if not isinstance(value,str) or not minlength<=len(value.strip())<=maxlength:raise ValueError(f'Escribe entre {minlength} y {maxlength} caracteres.')
    return value.strip()

def dispatch(path,data):
    if not isinstance(data,dict):raise ValueError('Se esperaba un objeto JSON.')
    if path=='/api/advanced/record':
        from . import advanced
        return advanced.record(sys.modules[__name__],data)
    if path=='/api/advanced/ai':
        from . import advanced
        return advanced.ai_dossier(sys.modules[__name__])
    if path=='/api/game/verify':
        from . import game
        return game.verify(sys.modules[__name__])
    if path=='/api/game/analysis':
        from . import game
        return game.analysis(sys.modules[__name__],data)
    if path=='/api/inject':
        if data.get('client_id') not in {c['id'] for c in CLIENTS}:raise ValueError('Cliente inválido.')
        twists={'salud':'El dueño informa que el procedimiento manual solo atiende al 20% de la demanda y otro centro comenzará a depender de esta API en el próximo turno.',
                'agua':'El dueño informa que la copia secundaria no puede abrirse. El repositorio accesible desde soporte es ahora la única vía de reconstrucción de la telemetría histórica.',
                'digital':'Un cliente esencial nuevo comparte la API. Su contrato reduce la tolerancia de interrupción a 15 minutos y exige separar sus expedientes de los demás.'}
        return save('context',{'client_id':data['client_id'],'text':twists[data['client_id']],'synthetic':True})
    if path=='/api/portfolio':
        if data.get('client_id') not in {c['id'] for c in CLIENTS}:raise ValueError('Cliente inválido.')
        packages=data.get('packages');costs={'A':(2,0),'B':(2,10),'C':(1,5),'D':(3,30)}
        if not isinstance(packages,list) or not packages or len(set(packages))!=len(packages) or any(x not in costs for x in packages):raise ValueError('Selecciona paquetes válidos y sin repetir.')
        hours=sum(costs[x][0] for x in packages);downtime=sum(costs[x][1] for x in packages)
        if hours>4 or downtime>15:raise ValueError(f'La cartera excede el caso: {hours} h / {downtime} min; máximo 4 h / 15 min. Diseña otra combinación.')
        return save('portfolio',{'client_id':data['client_id'],'packages':packages,'engineering_hours':hours,
                                 'downtime_minutes':downtime,'reason':nonempty(data.get('reason'),30),'synthetic_costs':True})
    if path=='/api/probe':
        action=data.get('action')
        routes={'transaction':('http://gateway:8080/api/transaction','edge'),
                'export':('http://gateway:8080/api/export','edge'),
                'diagnostics':('http://gateway:8080/api/diagnostics','edge'),
                'backup':('http://backup:8082/catalog','support')}
        if action not in routes:raise ValueError('Prueba fuera del alcance.')
        url,zone=routes[action]
        headers={'X-Training-Key':'training-backup-key'} if action=='backup' else {}
        result=request_target(url,headers=headers)
        return save('evidence',{'action':action,'zone':zone,'source':url,'result':result,
                    'observed':True,'content_sha256':hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()})
    if path=='/api/control':
        action=data.get('action');reason=nonempty(data.get('reason'),30)
        hosts={'restrict_export':['gateway'],'isolate_support':['gateway'],'rotate_backup':['backup'],'reset':['gateway','backup','records']}
        if action not in hosts:raise ValueError('Control fuera del alcance.')
        ports={'gateway':8080,'backup':8082,'records':8081}
        results=[request_target(f'http://{host}:{ports[host]}/_control',{'action':action},{'X-Lab-Control':CONTROL_KEY}) for host in hosts[action]]
        ok=all(x['status']==200 for x in results)
        return save('control',{'action':action,'reason':reason,'results':results,'ok':ok,
                             'meaning':'Cambio del simulador; requiere verificar ruta y función. No borra decisiones previas.'})
    if path=='/api/decisions':
        if data.get('client_id') not in {c['id'] for c in CLIENTS}:raise ValueError('Cliente inválido.')
        if data.get('finding_id') not in {f['id'] for f in FINDINGS if f['id'].startswith('F-')}:raise ValueError('Evalúa un hallazgo principal, no un duplicado.')
        reason=nonempty(data.get('reason'),30)
        owner=nonempty(data.get('owner'),3,150)
        evidence=data.get('evidence_ids')
        if not isinstance(evidence,list) or not evidence or any(x not in known_evidence() for x in evidence):raise ValueError('Elige evidencia existente. Las referencias inventadas no se guardan.')
        if data.get('state') not in ['inherent','residual']:raise ValueError('Estado de riesgo inválido.')
        result=evaluate(data)
        return save('decision',{k:data[k] for k in ['client_id','finding_id','likelihood','impacts','ssvc','state']}|{
            'reason':reason,'owner':owner,'evidence_ids':evidence,'calculation':result})
    if path=='/api/notes':
        task=data.get('task_id')
        if task not in {t['id'] for m in MISSIONS for t in m['tasks']}:raise ValueError('Misión inválida.')
        return save('note',{'id':'NOTE-'+task,'task_id':task,'answer':nonempty(data.get('answer'),30),
                            'formative':True,'grade':None})
    if path=='/api/triage':
        if data.get('finding_id') not in {f['id'] for f in FINDINGS}:raise ValueError('Hallazgo inválido.')
        if data.get('status') not in ['confirmed','under_investigation','duplicate','false_positive','present_not_reachable']:raise ValueError('Estado inválido.')
        return save('triage',{'finding_id':data['finding_id'],'status':data['status'],
                             'reason':nonempty(data.get('reason'),30)})
    if path=='/api/ai':
        client=data.get('client_id');ids=data.get('finding_ids',[])
        if client not in {c['id'] for c in CLIENTS}:raise ValueError('Cliente inválido.')
        if not isinstance(ids,list) or not 1<=len(ids)<=2 or any(i not in {f['id'] for f in FINDINGS} for i in ids):raise ValueError('Selecciona uno o dos hallazgos.')
        result=ai.propose(client,nonempty(data.get('question'),10,1000),ids)
        return save('ai',{'client_id':client,'finding_ids':ids,**result})
    if path=='/api/ai/review':
        item=next((x for x in records('ai') if x['id']==data.get('audit_id')),None)
        if not item:raise ValueError('Inferencia no encontrada.')
        if data.get('verdict') not in ['accept','correct','reject']:raise ValueError('Revisión inválida.')
        if item['validation_errors'] and data['verdict']=='accept':raise ValueError('La salida contiene errores estructurales o referencias inválidas: corrige o rechaza.')
        return save('review',{'audit_id':item['id'],'verdict':data['verdict'],'reason':nonempty(data.get('reason'),30)})
    if path=='/api/scan/import':
        report=data.get('report')
        if not isinstance(report,dict) or not isinstance(report.get('matches'),list):raise ValueError('Se requiere JSON real de Grype con matches[].')
        matches=report['matches']
        curated=[]
        for m in matches:
            if not isinstance(m,dict):raise ValueError('Cada match debe ser un objeto de Grype.')
            artifact=m.get('artifact',{});vulnerability=m.get('vulnerability',{})
            if not isinstance(artifact,dict) or not isinstance(vulnerability,dict):raise ValueError('Artifact y vulnerability deben ser objetos.')
            if str(artifact.get('name','')).lower() not in ['django','requests']:continue
            related=m.get('relatedVulnerabilities',[])
            if not isinstance(related,list):raise ValueError('relatedVulnerabilities debe ser una lista.')
            aliases=sorted({a['id'] for a in related if isinstance(a,dict) and isinstance(a.get('id'),str)})
            advisory=vulnerability.get('id')
            cves=sorted({a for a in aliases+([advisory] if isinstance(advisory,str) else []) if a.startswith('CVE-')})
            curated.append({'id':advisory,'aliases':aliases,'cve':cves[0] if cves else None,
                            'package':artifact.get('name'),'version':artifact.get('version'),'severity':vulnerability.get('severity')})
        return save('scan',{'source':'Grype importado por el alumno','matches_total':len(matches),'legacy_matches':curated,
                            'descriptor':report.get('descriptor',{}),'sha256':hashlib.sha256(json.dumps(report,sort_keys=True).encode()).hexdigest()})
    if path=='/api/risk/preview':return evaluate(data)
    raise ValueError('Acción no disponible.')


class Handler(BaseHTTPRequestHandler):
    def log_message(self,fmt,*args):print(fmt%args,flush=True)

    def send(self,obj,status=200):
        raw=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)

    def do_GET(self):
        path=urlsplit(self.path).path
        if path.startswith('/desktop/'):
            from .desktop_proxy import serve
            return serve(self)
        if path=='/api/access':
            from .access import metadata
            return self.send(metadata(sys.modules[__name__]))
        if path.startswith('/training/ssh/'):
            from .access import DOWNLOADS,serve_key
            if path in DOWNLOADS:return serve_key(self,path)
            return self.send({'error':'Archivo no disponible'},404)
        if path=='/api/game':
            from . import game
            return self.send(game.snapshot(sys.modules[__name__]))
        if path=='/health':return self.send({'ok':True,'version':'0.3.0'})
        if path=='/api/bootstrap':
            from .advanced import CONFIG
            intelligence=json.loads((ROOT/'data/intelligence.json').read_text())
            return self.send({'clients':CLIENTS,'findings':FINDINGS,'assets':ASSETS,'missions':MISSIONS,'corpus':CORPUS,
                'intelligence':intelligence,'advanced':{k:v for k,v in CONFIG.items() if k!='report_answers'},'version':'0.3.0','ssvc_tree':'DT_DP v1.0.0',
                'records':{k:records(k) for k in ['evidence','decision','note','ai','review','triage','control','scan','context','portfolio','station','game_campaign','game_activation','game_award','game_analysis','lab_event','lab_record']}})
        if path=='/api/advanced/layer':
            from . import advanced,game
            return self.send(advanced.layer(sys.modules[__name__],game.campaign(sys.modules[__name__])))
        if path=='/api/ai/status':return self.send(ai.status())
        if path=='/api/targets':return self.send({r:request_target(f'http://{r}:{port}/_status') for r,port in [('gateway',8080),('records',8081),('backup',8082)]})
        if path=='/api/export':return self.send(export_bundle())
        if path.startswith('/api/'):return self.send({'error':'Ruta no encontrada'},404)
        files={'/':'index.html','/favicon.svg':'favicon.svg','/anatomy.css':'anatomy.css','/context-figure.js':'context-figure.js','/game.js':'game.js','/advanced.js':'advanced.js','/game.css':'game.css'}
        if path not in files:return self.send({'error':'Archivo no encontrado'},404)
        f=ROOT/'web'/files[path];raw=f.read_bytes()
        self.send_response(200);self.send_header('Content-Type',{'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8','svg':'image/svg+xml'}[f.suffix[1:]])
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; frame-ancestors 'none'")
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)

    def do_POST(self):
        try:
            host=self.headers.get('Host','')
            hostname=urlsplit('http://'+host).hostname
            if hostname not in ['127.0.0.1','localhost','::1','mission']:
                return self.send({'error':'Usa localhost o 127.0.0.1.'},403)
            origin=self.headers.get('Origin')
            if origin and origin not in ['http://'+host,'https://'+host]:return self.send({'error':'Origen rechazado.'},403)
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send({'error':'Usa application/json.'},415)
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=8_000_000:return self.send({'error':'Cuerpo inválido o demasiado grande.'},413)
            payload=json.loads(self.rfile.read(length))
            return self.send(dispatch(urlsplit(self.path).path,payload))
        except (ValueError,KeyError,TypeError,StopIteration) as exc:self.send({'error':str(exc) or 'Datos incompletos.'},400)
        except Exception:
            import traceback;traceback.print_exc();self.send({'error':'No se pudo completar la operación. Revisa los logs del centro de misión.'},500)

if __name__=='__main__':
    connect().close()
    from .ssh_proxy import start
    start()
    ThreadingHTTPServer(('0.0.0.0',8000),Handler).serve_forever()
