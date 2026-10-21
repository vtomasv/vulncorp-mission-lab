"""Extensible campaign: real observations, explicit prerequisites and idempotent practice XP."""
import hashlib
import hmac
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,urlopen
from .secure import secret

CATALOG=json.loads((Path(__file__).resolve().parents[1]/'data/campaign.json').read_text())
CHALLENGES={c['id']:c for c in CATALOG['challenges']}
HOSTS={'analyst':'workstation','ops':'ops','appdesk':'appdesk'}
LOCK=threading.RLock()

def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()

def verified_envelope(envelope,station):
    event=envelope.get('event',{})
    if not isinstance(event,dict) or event.get('station')!=station:return False
    signature=envelope.get('signature','')
    expected=hmac.new(secret(station).encode(),canonical(event),hashlib.sha256).hexdigest()
    return isinstance(signature,str) and hmac.compare_digest(signature,expected)

def campaign(store):
    runs=store.records('game_campaign')
    if runs:return runs[-1]
    return store.save('game_campaign',{'started':time.time(),'catalog_version':CATALOG['version']})

def collect(store):
    known={x['id'] for x in store.records('station')};live={};addresses={}
    def station_read(pair):
        role,host=pair
        try:
            request=Request(f'http://{host}:9091/evidence',headers={'X-Station-Key':secret(role)})
            with urlopen(request,timeout=2) as response:return role,json.load(response)
        except (OSError,ValueError):return role,None
    with ThreadPoolExecutor(max_workers=3) as pool:
        for role,value in pool.map(station_read,HOSTS.items()):
            live[role]=value is not None
            if value:
                identity=value.get('identity',{})
                if verified_envelope(identity,role):
                    for address in identity['event'].get('addresses',[]):addresses[address]=role
                for envelope in value.get('proofs',[]):
                    if verified_envelope(envelope,role):
                        event=envelope['event']
                        if event['id'] not in known:
                            store.save('station',{**event,'signature':envelope['signature'],'provenance':'station-agent'});known.add(event['id'])
    existing={x['id'] for x in store.records('evidence')}
    for target,port in [('gateway',8080),('records',8081),('backup',8082)]:
        response=store.request_target(f'http://{target}:{port}/_audit',headers={'X-Lab-Control':store.CONTROL_KEY})
        for event in response.get('body',{}).get('events',[]):
            role=addresses.get(event.get('peer'))
            if not role or event['id'] in existing:continue
            route=event['path'];action={'/api/transaction':'transaction','/api/export':'export','/api/diagnostics':'diagnostics','/catalog':'backup'}.get(route)
            if not action:continue
            result={'status':event['status'],'body':event['body']}
            store.save('evidence',{'id':event['id'],'actor':role,'occurred_at':event['occurred_at'],'boot_id':event['boot_id'],
                'action':action,'zone':role,'source':f'http://{target}:{port}{route}','result':result,'observed':True,
                'provenance':'target-audit','content_sha256':hashlib.sha256(canonical(result)).hexdigest()})
            existing.add(event['id'])
    from . import advanced
    advanced.collect(store,addresses)
    return live

def current(store,run):
    awards={x['challenge_id'] for x in store.records('game_award') if x['run_id']==run['id']}
    return next((c for c in CATALOG['challenges'] if c['id'] not in awards and set(c['requires'])<=awards),None)

def activation(store,run,challenge):
    found=[x for x in store.records('game_activation') if x['run_id']==run['id'] and x['challenge_id']==challenge['id']]
    return found[-1] if found else store.save('game_activation',{'run_id':run['id'],'challenge_id':challenge['id'],'started':time.time()})

def conditions(store,challenge,run,active):
    records=lambda kind:[x for x in store.records(kind) if x.get('occurred_at',0)>=run['started'] or x.get('game_run')==run['id']]
    station=records('station');evidence=records('evidence')
    def command(action,role=None):return [x for x in station if x['action']==action and (not role or x['station']==role)]
    def observed(action,status,role='analyst',since=None):return [x for x in evidence if x.get('actor')==role and x['action']==action and x['result']['status']==status and (since is None or x['occurred_at']>=since)]
    checks=[]
    def check(label,ok,proofs=None):checks.append({'label':label,'ok':bool(ok),'proof_ids':[x['id'] for x in proofs or []]})
    id=challenge['id']
    if id=='contacto':
        rows=command('iniciar','analyst');check('Identidad comprobada desde tu puesto',any(x['result'].get('uid')==1000 for x in rows),rows)
    elif id=='funcion':
        rows=observed('transaction',200);check('Transacción completada desde análisis',any(x['result']['body'].get('status')=='completed' for x in rows),rows)
    elif id=='segmento':
        rows=command('red','analyst');valid=[]
        for row in rows:
            found={x['target']:x['result'] for x in row['result'].get('targets',[])}
            if found=={'gateway':'reachable','records':'not_resolved_in_this_zone','backup':'not_resolved_in_this_zone'}:valid.append(row)
        check('Segmentación observada desde análisis',valid,valid)
    elif id=='exposicion':
        check('Exportación sin autorización observada',observed('export',200),observed('export',200))
        check('Diagnóstico expuesto observado',observed('diagnostics',200),observed('diagnostics',200))
    elif id=='soporte':
        rows=command('red','ops');valid=[x for x in rows if {t['target'] for t in x['result'].get('targets',[]) if t['result']=='reachable'}=={'gateway','backup'}]
        check('Otra perspectiva comprobada desde soporte',valid,valid);check('Catálogo leído desde soporte',observed('backup',200,'ops'),observed('backup',200,'ops'))
    elif id=='inventario':
        rows=command('inventario','appdesk');valid=[x for x in rows if {p['name'].lower():p['version'] for p in x['result'].get('records_packages',[])}=={'django':'3.2','requests':'2.31.0'}]
        check('Syft identificó ambos componentes reales',valid,valid)
    elif id=='alertas':
        rows=command('escanear','appdesk');ids={v for row in rows for match in row['result'].get('matches',[]) for v in match['ids']}
        check('Grype ejecutado con reporte y procedencia',rows,rows)
        check('Aliases de las dos CVEs encontrados',{'CVE-2021-35042','CVE-2024-35195'}<=ids,rows)
    elif id=='aplicabilidad':
        rows=[x for x in command('revisar','appdesk') if x['result'].get('imports_legacy') is False]
        check('Código activo revisado y hash conservado',rows,rows)
    elif id in ['proveedor','expediente']:
        notes=records('game_analysis');latest=next((x for x in reversed(notes) if x.get('challenge_id')==id),None)
        if id=='proveedor':
            valid=[x for x in command('contrastar','appdesk') if x['result'].get('mission_packages')==[] and len(x['result'].get('records_packages',[]))==2]
            check('Inventarios de dos activos contrastados',valid,valid)
        check('Clasificaciones, fundamento y fuentes registrados',latest,[latest] if latest else [])
    elif id=='contexto':
        rows=records('decision');a=next((x for x in reversed(rows) if x['client_id']=='salud' and x['finding_id']=='F-02' and x['state']=='inherent'),None)
        b=next((x for x in reversed(rows) if x['client_id']=='agua' and x['finding_id']=='F-02' and x['state']=='inherent'),None)
        real={x['id'] for x in observed('export',200)}
        linked=a and b and all(real.intersection(x.get('evidence_ids',[])) for x in [a,b])
        check('Dos clientes evaluados con evidencia observada',linked,[x for x in [a,b] if x])
        check('El contexto cambia manteniendo L',a and b and a['likelihood']==b['likelihood'] and a['impacts']!=b['impacts'],[x for x in [a,b] if x])
    elif id=='asistente':
        proofs=command('ia','appdesk');audit_ids={p['result'].get('audit_id') for p in proofs if p['result'].get('live')}
        audits=[x for x in records('ai') if x['id'] in audit_ids and x['mode']=='live-local']
        reviews=[x for x in records('review') if x['audit_id'] in {a['id'] for a in audits}]
        check('Consulta real al modelo local desde aplicaciones',audits,audits)
        check('Revisión humana vinculada a la consulta',reviews,reviews)
    elif id=='cartera':
        rows=[x for x in records('portfolio') if 'A' in x.get('packages',[])];mapping=[x for x in records('game_analysis') if x.get('challenge_id')==id]
        check('Cartera dentro del presupuesto y la ventana',rows,rows);check('Alcance del control y fundamento registrados',mapping,mapping)
    elif id=='medida':
        rows=[x for x in command('proteger','appdesk') if x['result'].get('status')==200 and x['result'].get('action')=='restrict_export']
        check('Medida solicitada desde aplicaciones y confirmada',rows,rows)
    elif id=='continuidad':
        changes=[x for x in command('proteger','appdesk') if x['result'].get('status')==200]
        since=changes[-1]['occurred_at'] if changes else time.time()+1
        denied=observed('export',403,since=since);business=[x for x in observed('transaction',200,since=since) if x['result']['body'].get('status')=='completed']
        live=store.request_target('http://gateway:8080/_status')['body']
        check('Exportación 403 posterior al cambio',denied,denied)
        check('Transacción legítima completada después',business,business)
        check('La restricción continúa activa',live.get('state',{}).get('restrict_export'))
        denied_ids={x['id'] for x in denied};business_ids={x['id'] for x in business}
        residual=[x for x in records('decision') if x['finding_id']=='F-02' and x['state']=='residual' and denied_ids.intersection(x['evidence_ids']) and business_ids.intersection(x['evidence_ids'])]
        check('Residual registrado con ambas pruebas',residual,residual)
    from . import advanced
    return checks or advanced.conditions(store,challenge,run)

def snapshot(store,live=None,feedback=None):
    run=campaign(store);awards=[x for x in store.records('game_award') if x['run_id']==run['id']]
    done={x['challenge_id'] for x in awards};next_item=current(store,run)
    if next_item:activation(store,run,next_item)
    return {'catalog':CATALOG,'run':run,'awards':awards,'xp':sum(x['xp'] for x in awards),'total_xp':sum(c['xp'] for c in CATALOG['challenges']),
        'current':next_item['id'] if next_item else None,'completed':len(done),'total':len(CHALLENGES),'stations':live or {},'feedback':feedback,
        'states':{c['id']:('done' if c['id'] in done else 'active' if set(c['requires'])<=done else 'locked') for c in CATALOG['challenges']}}

def verify(store):
    with LOCK:
        run=campaign(store);item=current(store,run)
        if not item:return snapshot(store)
        active=activation(store,run,item);live=collect(store);checks=conditions(store,item,run,active)
        passed=bool(checks) and all(c['ok'] for c in checks)
        feedback={'challenge_id':item['id'],'checks':checks,'passed':passed,'checked_at':time.time()}
        if passed:
            award_id='XP-'+run['id']+'-'+item['id']
            if not any(x['id']==award_id for x in store.records('game_award')):
                store.save('game_award',{'id':award_id,'run_id':run['id'],'challenge_id':item['id'],'xp':item['xp'],'checks':checks,
                    'meaning':'Hito de práctica, sin efecto en la nota. La argumentación no se califica automáticamente.'})
        return snapshot(store,live,feedback)

def analysis(store,data):
    run=campaign(store);item=current(store,run)
    if not item or data.get('challenge_id')!=item['id']:raise ValueError('Registra el análisis del objetivo activo.')
    text=store.nonempty(data.get('reason'),40)
    if item['id']=='proveedor':
        if data.get('duplicate')!='VENDOR-06' or data.get('misattributed')!='VENDOR-07':raise ValueError('Contrasta activo, componente y versión. La evidencia todavía no sostiene esa clasificación.')
    elif item['id']=='expediente':
        if data.get('component')!='present_not_reachable' or data.get('local')!='confirmed':raise ValueError('Distingue componente presente de falla de autorización reproducida.')
        refs=data.get('evidence_ids',[])
        real={x['id'] for x in store.records('evidence') if x.get('occurred_at',0)>=run['started'] and x.get('actor')=='analyst' and x['action']=='export' and x['result']['status']==200}
        if not isinstance(refs,list) or not real.intersection(refs):raise ValueError('Vincula una exportación observada desde análisis.')
    elif item['id']=='cartera':
        if any(data.get(k)!=v for k,v in {'mitre':'T1190','iso':'A.8.26','law':'L21663_8'}.items()):raise ValueError('Revisa conducta hipotética, objetivo del control y marco de gestión OIV. Una asociación no acredita cumplimiento.')
        if data.get('scope')!='http_only':raise ValueError('La prueba de una ruta HTTP no acredita por sí sola segmentación de red.')
    else:raise ValueError('Ese objetivo no usa este formulario.')
    fields=['challenge_id','duplicate','misattributed','component','local','evidence_ids','scope','mitre','iso','law']
    body={k:data[k] for k in fields if k in data}
    return store.save('game_analysis',{**body,'reason':text,'game_run':run['id'],'checked':'Estructura y relaciones comprobadas; calidad del argumento para discusión.'})
