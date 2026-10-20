"""Teacher/developer integration check. Creates a NEW campaign; never deletes historical evidence.
Core: real SSH, segmentation, target audit and XP. --full additionally needs prepared Grype + local model.
"""
import argparse
import json
import subprocess
from pathlib import Path
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8095'

def dc(*args,input=None,timeout=300):
    result=subprocess.run(['docker','compose',*args],cwd=ROOT,input=input,text=True,capture_output=True,timeout=timeout)
    if result.returncode:raise AssertionError(result.stderr[-1800:]+'\n'+result.stdout[-1800:])
    return result.stdout

def api(path,data=None):
    request=Request(BASE+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with urlopen(request,timeout=300) as response:return json.load(response)

def station(*args,input=None):return dc('exec','-T','-u','1000','workstation',*args,input=input)

def fresh(label='Verificación técnica'):
    dc('exec','-T','mission','python','-c',"import time;from app.server import save;save('game_campaign',{'started':time.time(),'catalog_version':'2.0','purpose':"+repr(label)+"})")
    api('/api/control',{'action':'reset','reason':'Preparar una nueva ejecución de validación conservando todo el historial.'})
    return api('/api/game')

def credit(id):
    result=api('/api/game/verify',{})
    assert result['states'][id]=='done',(id,result.get('feedback'))
    print(f"PASS {id}: {result['completed']}/{result['total']} · {result['xp']} PX",flush=True)
    return result

def payload(client,impacts,proofs,state='inherent',likelihood=4):
    return {'client_id':client,'finding_id':'F-02','state':state,'likelihood':likelihood,'impacts':dict(zip(['operation','people','data','financial'],impacts)),
        'ssvc':dict(exploitation='P',exposure='O' if state=='inherent' else 'C',automatable='Y',human_impact='H' if client=='salud' else 'L'),
        'reason':'La prueba observada permite sostener el acceso indebido o su mitigación. El dueño debe validar las consecuencias y aceptar el residual; la causa raíz permanece pendiente.',
        'owner':'Dueño sintético de validación','evidence_ids':proofs}

def main(full=False):
    initial=fresh();assert initial['xp']==0
    # A request made by the management plane must not award a workstation task.
    api('/api/probe',{'action':'transaction'});assert api('/api/game/verify',{})['xp']==0
    station('lab','iniciar');credit('contacto')
    station('curl','-fsS','http://gateway:8080/api/transaction');credit('funcion')
    station('lab','red');credit('segmento')
    station('curl','-fsS','http://gateway:8080/api/export');station('curl','-fsS','http://gateway:8080/api/diagnostics');credit('exposicion')
    station('ssh','ops','lab red');station('ssh','ops',"curl -fsS -H 'X-Training-Key: training-backup-key' http://backup:8082/catalog");result=credit('soporte')
    for role in ['ops','appdesk']:
        assert 'uid=1000(student)' in station('ssh','-tt',role,'id')
    # Student cannot read a signing secret, a private journal or become root.
    for path in ['/secrets/analyst.key','/journal/events.jsonl']:
        denied=subprocess.run(['docker','compose','exec','-T','-u','1000','workstation','cat',path],cwd=ROOT,capture_output=True)
        assert denied.returncode!=0,path
    appnets=json.loads(dc('exec','-T','-u','1000','workstation','ssh','appdesk','lab red').split('Evidencia registrada:')[0].split('evidencia.\n',1)[1])
    assert {t['target'] for t in appnets['targets'] if t['result']=='reachable'}=={'gateway','records'}
    if full:
        station('ssh','appdesk','lab inventario');credit('inventario')
        station('ssh','appdesk','lab escanear');credit('alertas')
        station('ssh','appdesk','lab revisar');credit('aplicabilidad')
        station('ssh','appdesk','lab contrastar')
        api('/api/game/analysis',{'challenge_id':'proveedor','duplicate':'VENDOR-06','misattributed':'VENDOR-07','reason':'Los inventarios reales muestran dos componentes en records y ninguno de esos dos en mission. La combinación de activo, versión y CVE repite el mismo trabajo.'});credit('proveedor')
        proofs=api('/api/bootstrap')['records']['evidence'];export=next(x for x in reversed(proofs) if x.get('actor')=='analyst' and x['action']=='export' and x['result']['status']==200)
        api('/api/game/analysis',{'challenge_id':'expediente','component':'present_not_reachable','local':'confirmed','reason':'La presencia del componente no acredita alcanzabilidad. En cambio la exportación entrega registros ficticios sin autorización desde análisis.','evidence_ids':[export['id']]});credit('expediente')
        for client,impacts in [('salud',[4,3,4,3]),('agua',[2,1,2,2])]:api('/api/decisions',payload(client,impacts,[export['id']]))
        credit('contexto')
        station('ssh','appdesk','lab ia');api('/api/game/verify',{})
        audit=next(x for x in reversed(api('/api/bootstrap')['records']['ai']) if x.get('game_run')==initial['run']['id'])
        assert audit['mode']=='live-local' and audit['model_digest_verified']
        api('/api/ai/review',{'audit_id':audit['id'],'verdict':'correct','reason':'La referencia es material del caso, no prueba de una observación. Contrasto la hipótesis con la exportación real y mantengo pendiente la aceptación del dueño.'});credit('asistente')
        api('/api/portfolio',{'client_id':'salud','packages':['A','B'],'reason':'Proteger la exportación y la recuperación dentro de cuatro horas y diez minutos de ventana.'})
        api('/api/game/analysis',{'challenge_id':'cartera','scope':'http_only','mitre':'T1190','iso':'A.8.26','law':'L21663_8','reason':'La restricción HTTP limita una ruta observada y orienta la revisión de autorización. No demuestra segmentación de red ni cumplimiento integral de controles o leyes.'});credit('cartera')
        station('ssh','appdesk','lab proteger',input='Restringir temporalmente exportación; después verificar denegación y transacción legítima.\n');credit('medida')
        station('curl','-s','http://gateway:8080/api/export');station('curl','-fsS','http://gateway:8080/api/transaction');api('/api/game/verify',{})
        records=api('/api/bootstrap')['records']['evidence'];denied=next(x for x in reversed(records) if x.get('actor')=='analyst' and x['action']=='export' and x['result']['status']==403);business=next(x for x in reversed(records) if x.get('actor')=='analyst' and x['action']=='transaction' and x['result']['body'].get('status')=='completed')
        api('/api/decisions',payload('salud',[4,3,4,3],[denied['id'],business['id']],'residual',2));result=credit('continuidad')
        assert result['completed']==result['total'] and result['xp']==result['total_xp']
        for _ in range(3):assert api('/api/game/verify',{})['xp']==result['xp']
        result['validated_ai']={k:audit[k] for k in ['id','model','model_digest','elapsed_seconds','validation_errors']}
    (ROOT/'artifacts').mkdir(exist_ok=True)
    (ROOT/'artifacts/validation-game.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('PASS campaña completa con Grype e IA local' if full else 'PASS núcleo real: 5 objetivos, tres puestos, aislamiento y permisos')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args();main(args.full)
