"""Real new range via host SSH. The first 15 awards are an EXPLICIT TEST FIXTURE.

No previous lab is claimed as revalidated here. Uses a separate campaign, preserves
all history and restores the previously selected campaign in finally. --full also
executes the final local-model inference. ZAP must already be running.
"""
import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError
from tests import integration_game as base
from app.advanced import CONFIG

ROOT=Path(__file__).resolve().parents[1]


def mutation(code):return base.dc('exec','-T','mission','python','-c',code)
def command(action):
    text=base.station('ssh','appdesk','lab '+action)
    print('REAL SSH:',action,flush=True)
    return text
def latest():return base.api('/api/bootstrap')['records']
def events(run):
    base.api('/api/game/verify',{})
    return [r for r in latest()['lab_event'] if r.get('campaign')==run]
def answers(id,rows):
    value={f['key']:f.get('expected',f['options'][0][0] if 'options' in f else 'La observación y su fuente permiten sostener una conclusión acotada; no se atribuye cumplimiento ni actividad fuera de la simulación.') for p in CONFIG['exercises'][id]['pages'] for f in p['fields']}
    if id=='cronologia':value['order']='\n'.join(r['id'] for r in rows if r['kind']=='document' and r.get('correlation','').startswith('SIM-'))
    if id=='mapeo':
        for key,identity in [('t1190','training-agua-user'),('t1078','training-stolen-salud')]:
            value[key]=next(r['id'] for r in rows if r.get('identity')==identity and r.get('correlation','').startswith('SIM-'))
    if id=='reportes':value.update(CONFIG['report_answers'])
    if id=='matriz':
        for fid,ref in [('F-01','EV-PACKAGES'),('F-02','EV-EXPORT'),('F-03','EV-BACKUP'),('F-04','EV-DIAGNOSTICS'),('F-05','EV-ARCHITECTURE')]:
            value[fid+'_reason']=ref+' es un fragmento del caso; lo diferencio de la observación de estación. La asociación orienta el control y todavía exige probar su eficacia.'
    if id=='excepcion':value['expiry']='2026-11-10T12:00:00Z'
    if id=='auditoria':value['reason']='LAW-ART9 delimita plazos de reporte, no demuestra cumplimiento. La prueba HTTP sustenta accesos observados, no todos los efectos de negocio del guion.'
    return value


def main(full=False, keep=False):
    base.USE_SSH=True
    original=base.api('/api/game')['run']
    mutation("import time;from app.server import save;from app.game import CATALOG;run=save('game_campaign',{'started':time.time(),'catalog_version':'3.0','purpose':'VALIDATION-4-6; first 15 awards are test fixture'});[save('game_award',{'run_id':run['id'],'challenge_id':c['id'],'xp':c['xp'],'test_fixture':True}) for c in CATALOG['challenges'][:15]]")
    run=base.api('/api/game')['run']['id']
    report={'run':run,'fixture':'First 15 awards only; no learner evidence fabricated for new goals.','entry':'Host SSH -> analyst -> appdesk','full_ai':full,'goals':[]}
    try:
        # A new target is not exposed directly from the edge station.
        denied=base.station('sh','-c','getent hosts validation collector webscan || true')
        assert not any(name in denied for name in ['validation','collector','webscan']),denied
        for id in CONFIG['exercises']:
            if id=='auditoria' and not full:break
            actions={'alcance':['abrir'],'callback':['callback'],'marcador':['marcador'],'tenants':['transferencia'],'contraste-zap':['zap'],
                     'simulacion':['simular'],'cronologia':['cronologia'],'autorizacion':['ensayar','corregir','ensayar'],
                     'revocacion':['revocar','ensayar'],'capa':['capa'],'incidente':['incidente'],'auditoria':['ia-expediente']}.get(id,[])
            for action in actions:command(action)
            rows=events(run)
            refs=[r['id'] for r in rows if r['kind'] in ['document','request','marker','collector','callback']]
            payload={'challenge_id':id,'answers':answers(id,rows),'evidence_ids':refs[-30:]}
            if id=='alcance':payload['evidence_ids']=[]
            if id=='mapeo':payload['evidence_ids']=list(dict.fromkeys(refs[-26:]+[payload['answers']['t1190'],payload['answers']['t1078']]))
            # An arbitrary browser proof can never replace a target event.
            if id=='callback':
                try:base.api('/api/advanced/record',{**payload,'evidence_ids':['RNG-forged']})
                except HTTPError as exc:assert exc.code==400
                else:raise AssertionError('Invented evidence accepted')
            base.api('/api/advanced/record',payload)
            result=base.credit(id)
            if id=='autorizacion':
                episode=next(r['episode'] for r in rows)
                base.dc('restart','validation','collector')
                # Startup is bounded and subsequent real actions must retain episode and controls.
                for _ in range(20):
                    state=json.loads(mutation("import json;from app.server import request_target,CONTROL_KEY;print(json.dumps(request_target('http://validation:8083/_status',headers={'X-Lab-Control':CONTROL_KEY})))"))
                    if state.get('status')==200:break
                    time.sleep(.5)
                assert state['body']['state']['episode']==episode and state['body']['state']['authz_fixed']
                report['range_survives_restart']=True
            before=result['xp'];assert base.api('/api/game/verify',{})['xp']==before
            report['goals'].append(id)
        rows=events(run)
        assert any(r['kind']=='marker' and r.get('output')=='TRAINING-MARKER-ONLY' for r in rows)
        layer=base.api('/api/advanced/layer');assert {r['techniqueID'] for r in layer['techniques']}=={'T1190','T1078'}
        report['layer']=layer
        report['event_count']=len(rows)
        report['export']=base.api('/api/export')
        if full:assert len(report['goals'])==18
        (ROOT/'artifacts/validation-advanced.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print('PASS new goals:',len(report['goals']),'· genuine range events:',len(rows),'· local AI:',full,flush=True)
    finally:
        if not keep:
            mutation('from app.server import save;save("game_campaign",'+repr(original)+')')
            command('abrir')
            print('Restored previous campaign; all validation history preserved.',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');p.add_argument('--keep-test-campaign',action='store_true');args=p.parse_args();main(args.full,args.keep_test_campaign)
