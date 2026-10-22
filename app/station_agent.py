"""Agent of a training station. Learner calls a local Unix socket; UI can only read signed results.

No arbitrary command, path or target is accepted. The agent's key/journal are outside
learner ownership. This protects normal learning evidence, not a hostile Docker host owner.
"""
import ast
import socket
import fcntl
import hashlib
import hmac
import json
import os
import socketserver
import struct
import subprocess
import threading
import time
import uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from . import cli
from .secure import secret

ROLE=os.environ.get('LAB_STATION','analyst')
KEY=secret(ROLE)
JOURNAL=Path('/journal/events.jsonl')
LOCK=threading.Lock()
ACTIONS=threading.Lock()

def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()

def sign(event):return hmac.new(KEY.encode(),canonical(event),hashlib.sha256).hexdigest()

def emit(action,result):
    event={'id':'ST-'+uuid.uuid4().hex,'station':ROLE,'action':action,'occurred_at':time.time(),'result':result}
    envelope={'event':event,'signature':sign(event)}
    with LOCK:
        with JOURNAL.open('a') as f:f.write(json.dumps(envelope,ensure_ascii=False)+'\n')
    return event['id']

def tool(argv,timeout=120):
    result=subprocess.run(argv,capture_output=True,text=True,timeout=timeout,
        user=1000,group=1000,extra_groups=[],env={**os.environ,'HOME':'/home/student','LC_ALL':'C.UTF-8'})
    if result.returncode:raise ValueError((result.stderr or result.stdout)[-1800:] or 'La herramienta devolvió un error.')
    return result.stdout

def write_student(name,value):
    path=Path('/home/student/evidence')/name
    # Never follow learner-controlled links while running the agent as root.
    root=Path('/home/student/evidence')
    if root.is_symlink() or root.resolve()!=root:raise ValueError('La carpeta de evidencia debe ser un directorio normal.')
    raw=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as f:f.write(raw)
    os.chown(path,1000,1000,follow_symlinks=False)
    return str(path)

def http(url,data=None,headers=None,timeout=10):
    req=Request(url,data=json.dumps(data).encode() if data is not None else None,
        headers={'Content-Type':'application/json',**(headers or {})})
    try:
        with urlopen(req,timeout=timeout) as response:return response.status,json.load(response)
    except HTTPError as exc:
        try:body=json.load(exc)
        except ValueError:body={'error':str(exc)}
        return exc.code,body

def packages(bom):
    return sorted([{'name':p['name'],'version':p.get('version'),'purl':p.get('purl')}
        for p in bom.get('components',[]) if p.get('name','').lower() in ['django','requests']],key=lambda p:p['name'].lower())

def execute(data):
    action=data.get('action')
    from . import continuation_station
    if ROLE=='appdesk' and action in continuation_station.COMMANDS:
        import sys
        result,text=continuation_station.execute(action,sys.modules[__name__])
        return {'ok':True,'stdout':text,'proof_id':emit(action,result)}
    from . import advanced_station
    if ROLE=='appdesk' and action in advanced_station.ACTIONS:
        import sys
        result,text=advanced_station.execute(action,sys.modules[__name__])
        return {'ok':True,'stdout':text,'proof_id':emit(action,result)}
    allowed={'analyst':{'iniciar','red'},'ops':{'iniciar','red'},
        'appdesk':{'iniciar','red','inventario','escanear','revisar','contrastar','ia','proteger'}}
    if action not in allowed.get(ROLE,set()):raise ValueError('Ese comando pertenece a otro puesto. Escribe lab ayuda y revisa el objetivo.')
    if action=='iniciar':
        out=tool(['id'])+'\n'+tool(['hostname'])
        result={'uid':1000,'station':ROLE,'stdout':out};text=out+'\nPuesto listo. Elige el siguiente objetivo en el laboratorio.'
    elif action=='red':
        result=cli.discover();result['zone']=ROLE;text=json.dumps(result,ensure_ascii=False,indent=2)
    elif action in ['inventario','contrastar']:
        bom=json.loads(tool(['syft','dir:/company/records-root','-o','cyclonedx-json']))
        result={'scope':'Copia parcial y de solo lectura del filesystem legacy de records; no es el SBOM completo de la imagen.',
            'tool':tool(['syft','version']).strip(),'records_packages':packages(bom),
            'bom_sha256':hashlib.sha256(canonical(bom)).hexdigest()}
        path=write_student('records.cdx.json',bom)
        if action=='contrastar':
            other=json.loads(tool(['syft','dir:/company/mission-root','-o','cyclonedx-json']))
            result['mission_packages']=packages(other)
            write_student('mission.cdx.json',other)
        text=json.dumps(result,ensure_ascii=False,indent=2)+'\n\nSBOM real guardado en '+path
    elif action=='escanear':
        # Generate a fresh SBOM inside the trusted action; do not trust a file edited by the learner.
        bom=json.loads(tool(['syft','dir:/company/records-root','-o','cyclonedx-json']))
        canonical_path=Path('/journal/current-bom.json');canonical_path.write_bytes(canonical(bom));canonical_path.chmod(0o644)
        # /journal is private. Pass the SBOM on stdin instead of granting the learner access.
        proc=subprocess.run(['grype','-o','json'],input=json.dumps(bom),capture_output=True,text=True,
            timeout=180,user=1000,group=1000,extra_groups=[],env={**os.environ,'HOME':'/home/student','GRYPE_DB_AUTO_UPDATE':'false'})
        if proc.returncode:raise ValueError('Grype no pudo completar el escaneo. El docente debe preparar su base con ./lab.sh prepare-game. Detalle: '+proc.stderr[-900:])
        report=json.loads(proc.stdout);matches=[]
        for m in report.get('matches',[]):
            ids={m.get('vulnerability',{}).get('id','')}|{x.get('id','') for x in m.get('relatedVulnerabilities',[])}
            matches.append({'ids':sorted(ids- {''}),'package':m.get('artifact',{}).get('name'),'version':m.get('artifact',{}).get('version')})
        result={'matches':matches,'matches_total':len(matches),'report_sha256':hashlib.sha256(canonical(report)).hexdigest(),
            'descriptor':report.get('descriptor',{}),'scope':'Snapshot parcial real de records; no escaneo de Internet.'}
        path=write_student('grype-records.json',report)
        text=json.dumps(result,ensure_ascii=False,indent=2)+'\n\nReporte auténtico guardado en '+path
    elif action=='revisar':
        path=Path('/company/active-service/targets.py');source=path.read_text();tree=ast.parse(source)
        imports=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
            if isinstance(node,ast.ImportFrom):imports.append(node.module or '')
        result={'imports':sorted(set(imports)),'imports_legacy':any(x.split('.')[0] in ['django','requests'] for x in imports),
            'code_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'limit':'Revisión estática del archivo mostrado; no demuestra ausencia universal de uso ni de compromiso.'}
        text=json.dumps(result,ensure_ascii=False,indent=2)
    elif action=='ia':
        status,body=http('http://mission:8000/api/ai',{'client_id':'salud','finding_ids':['F-02'],
            'question':'¿Qué debo preguntar al dueño antes de priorizar? Distingue hipótesis y observaciones; propone tratamientos y cita las fuentes recibidas.'},timeout=250)
        if status!=200:raise ValueError(body.get('error','El modelo local no está disponible.'))
        result={'audit_id':body['id'],'model':body['model'],'digest':body['model_digest'],'live':body['mode']=='live-local'}
        text=json.dumps(body['output'],ensure_ascii=False,indent=2)+'\n\nConsulta '+body['id']+'. Revisa sus fuentes en el objetivo del juego.'
    elif action=='proteger':
        reason=data.get('reason','')
        if not isinstance(reason,str) or not 30<=len(reason.strip())<=4000:raise ValueError('Explica el motivo y las pruebas posteriores con al menos 30 caracteres.')
        status,body=http('http://gateway:8080/_control',{'action':'restrict_export'},{'X-Lab-Control':secret('control')})
        if status!=200 or not body.get('ok'):raise ValueError('El servicio no confirmó la medida. No se acredita un cambio.')
        result={'action':'restrict_export','reason':reason.strip(),'status':status,'ack':body,'root_cause_fixed':False}
        text='El gateway confirmó la restricción de exportación. Ahora vuelve al puesto de análisis y comprueba acceso y función. La autorización de records sigue pendiente.'
    event_id=emit(action,result)
    return {'ok':True,'stdout':text,'proof_id':event_id}

class Local(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            _,uid,_=struct.unpack('3i',self.request.getsockopt(__import__('socket').SOL_SOCKET,__import__('socket').SO_PEERCRED,12))
            if uid not in [0,1000]:raise ValueError('Usuario del puesto no autorizado.')
            raw=self.rfile.readline(8001)
            if len(raw)>8000:raise ValueError('Solicitud demasiado grande.')
            data=json.loads(raw)
            if not isinstance(data,dict):raise ValueError('Se esperaba una acción local.')
            if not ACTIONS.acquire(blocking=False):raise ValueError('Ya hay una herramienta trabajando en este puesto. Espera su resultado.')
            try:result=execute(data)
            finally:ACTIONS.release()
        except (OSError,ValueError,KeyError,subprocess.TimeoutExpired) as exc:result={'ok':False,'error':str(exc)}
        self.wfile.write(json.dumps(result,ensure_ascii=False).encode())

def identity():
    addresses=[]
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        for _,name in socket.if_nameindex():
            if name=='lo':continue
            try:
                value=fcntl.ioctl(sock.fileno(),0x8915,struct.pack('256s',name[:15].encode()))
                addresses.append(socket.inet_ntoa(value[20:24]))
            except OSError:pass
    public_key=Path('/journal/host_ed25519.pub')
    event={'id':'station-identity','station':ROLE,'addresses':addresses,'occurred_at':time.time(),
        'ssh_host_key':public_key.read_text().strip() if public_key.is_file() else None}
    return {'event':event,'signature':sign(event)}

class Reader(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/health':value={'ok':True,'station':ROLE}
        elif self.path=='/identity' and hmac.compare_digest(self.headers.get('X-Station-Key',''),KEY):value=identity()
        elif self.path=='/evidence' and hmac.compare_digest(self.headers.get('X-Station-Key',''),KEY):
            with LOCK:value={'station':ROLE,'identity':identity(),'proofs':[json.loads(line) for line in JOURNAL.read_text().splitlines()] if JOURNAL.exists() else []}
        else:self.send_error(403);return
        raw=json.dumps(value,ensure_ascii=False).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def log_message(self,*args):pass

if __name__=='__main__':
    JOURNAL.parent.mkdir(parents=True,exist_ok=True);JOURNAL.parent.chmod(0o700)
    socket_path='/run/lab-agent.sock'
    Path(socket_path).unlink(missing_ok=True)
    local=socketserver.ThreadingUnixStreamServer(socket_path,Local)
    os.chown(socket_path,0,1000);os.chmod(socket_path,0o660)
    threading.Thread(target=local.serve_forever,daemon=True).start()
    ThreadingHTTPServer(('0.0.0.0',9091),Reader).serve_forever()
