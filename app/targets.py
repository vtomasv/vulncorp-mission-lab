"""Servicios deliberadamente defectuosos. Solo en redes Docker aisladas."""
import json
import os
import threading
import time
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

ROLE = os.environ.get('LAB_ROLE','gateway')
PORTS = {'gateway':8080,'records':8081,'backup':8082}
LOCK = threading.Lock()
STATE = {'restrict_export':False,'isolate_support':False,'rotate_backup':False,'transactions':0}
CONTROL_KEY = os.environ.get('LAB_CONTROL_KEY','synthetic-control-key-not-for-production')


class Target(BaseHTTPRequestHandler):
    server_version='VulnCorpTraining/0.1'

    def log_message(self, fmt, *args):
        print(json.dumps({'time':time.time(),'role':ROLE,'path':self.path,'message':fmt%args}),flush=True)

    def reply(self, data, status=200):
        raw=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)

    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/health':return self.reply({'ok':True,'role':ROLE,'version':'0.1.0'})
        if path=='/_status':return self.reply({'role':ROLE,'state':STATE})
        if ROLE=='gateway':
            if path in ['/','/api/catalog']:
                return self.reply({'service':'VulnCorp Trámites','synthetic':True,'items':['resultado-urgente','documento-operacional','transferencia-cliente'],'message':'Portal público simulado. No contiene datos reales.'})
            if path=='/api/diagnostics':
                if STATE['isolate_support']:return self.reply({'error':'Ruta de soporte restringida'},403)
                return self.reply({'warning':'Diagnóstico expuesto por error','services':PORTS,'legacy':'Django 3.2 en records; función analytics deshabilitada'})
            if path in ['/api/export','/api/transaction']:
                if path=='/api/export' and STATE['restrict_export']:
                    return self.reply({'error':'Exportación pública restringida temporalmente','root_cause_fixed':False},403)
                endpoint='/export' if path=='/api/export' else '/transaction'
                try:
                    with urllib.request.urlopen('http://records:8081'+endpoint,timeout=3) as r:
                        return self.reply(json.load(r),r.status)
                except (OSError,ValueError):return self.reply({'error':'Dependencia records no disponible','business_function':'degraded'},503)
        if ROLE=='records':
            if path=='/export':
                return self.reply({'synthetic':True,'authentication_checked':False,'tenant':'sur',
                    'records':[{'id':'SYN-101','name':'PERSONA FICTICIA UNO','result':'RESULTADO DE ENTRENAMIENTO'},
                               {'id':'SYN-102','name':'PERSONA FICTICIA DOS','result':'RESULTADO DE ENTRENAMIENTO'}]})
            if path=='/transaction':
                with LOCK:STATE['transactions']+=1;n=STATE['transactions']
                return self.reply({'status':'completed','transaction_id':f'TRAIN-{n:04d}','synthetic':True,'dependency':'records'})
        if ROLE=='backup' and path=='/catalog':
            expected='rotated-training-key' if STATE['rotate_backup'] else 'training-backup-key'
            if self.headers.get('X-Training-Key')!=expected:return self.reply({'error':'Llave rechazada'},403)
            return self.reply({'synthetic':True,'account':'shared-support' if not STATE['rotate_backup'] else 'backup-reader',
                'permissions':['read','delete'] if not STATE['rotate_backup'] else ['read'],
                'copies':[{'name':'recovery-training-001','status':'catalogued','restore_tested':False}],
                'note':'Catálogo, no restauración real. Borrado no implementado en clases 1-3.'})
        self.reply({'error':'Ruta no disponible'},404)

    def do_POST(self):
        if self.path!='/_control' or self.headers.get('X-Lab-Control')!=CONTROL_KEY:
            return self.reply({'error':'Control de entrenamiento no autorizado'},403)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=4096:raise ValueError()
            data=json.loads(self.rfile.read(length));action=data['action']
            if action not in ['restrict_export','isolate_support','rotate_backup','reset']:raise ValueError()
            with LOCK:
                if action=='reset':STATE.update(restrict_export=False,isolate_support=False,rotate_backup=False,transactions=0)
                else:STATE[action]=True
            self.reply({'ok':True,'role':ROLE,'state':STATE})
        except (KeyError,ValueError,TypeError):self.reply({'error':'Acción inválida'},400)


if __name__=='__main__':
    ThreadingHTTPServer(('0.0.0.0',PORTS[ROLE]),Target).serve_forever()
