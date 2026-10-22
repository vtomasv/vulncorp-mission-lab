"""Real host SSH -> analyst -> appdesk -> fixed controller -> real PHP.

First 33 awards are explicitly a TEST FIXTURE, never a revalidation of labs 1–6.
Default also skips five AI-dependent goals using award fixtures only (no invented
inference or evidence). --full executes all 24 goals with three local inferences.
Separate campaign; previous selection and all history are preserved.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from tests import integration_game as base
from app.continuation import CONFIG, canonical

ROOT=Path(__file__).resolve().parents[1]
AI_GOALS={'ia-base','ia-hostil','revision-ia','frontera-ia','cierre-ia'}
ACTIONS={
 'encargo-ia':['mision-abrir'],'fuentes-php':['php-fuentes'],'ia-base':['ia-base'],'ia-hostil':['ia-hostil'],
 'frontera-ia':['ia-frontera'],'php-inventario':['php-inventariar'],'php-linea-base':['php-ensayar'],
 'php-mitigacion':['php-mitigar'],'php-despliegue':['php-desplegar'],'php-verificacion':['php-validar'],
 'ops-cambio':['ops-deriva'],'ops-residual':['ops-contener'],'ops-copia':['ops-copiar'],
 'ops-interrupcion':['ops-danar'],'ops-restauracion':['ops-restaurar'],'ops-metricas':['ops-metricas'],
 'cierre-alcance':['cierre-caso'],'cierre-contraprueba':['cierre-probar'],'cierre-ia':['cierre-ia'],'cierre-dossier':['cierre-exportar']}

def mutation(code):return base.dc('exec','-T','mission','python','-c',code)
def command(action):
    result=base.station('ssh','appdesk','lab '+action);print('REAL SSH:',action,flush=True);return result

def main(full=False):
    base.USE_SSH=True;original=base.api('/api/game')['run']
    mutation("import time;from app.server import save;from app.game import CATALOG;r=save('game_campaign',{'started':time.time(),'catalog_version':'4.0','purpose':'VALIDATION-7-10; previous 33 awards fixture'});[save('game_award',{'run_id':r['id'],'challenge_id':c['id'],'xp':c['xp'],'test_fixture':True}) for c in CATALOG['challenges'][:33]]")
    run=base.api('/api/game')['run']['id'];report={'run':run,'full_ai':full,'fixtures':['previous 33 awards'],'real_goals':[],'inferences':[]}
    try:
        for role in ['workstation','appdesk']:
            denied=base.dc('exec','-T','-u','1000',role,'sh','-c','getent hosts php-legacy php-patched || true')
            assert not denied.strip(),denied
        try:base.api('/api/continuation/action',{'action':'php-desplegar'})
        except HTTPError as exc:assert exc.code==403
        else:raise AssertionError('Browser gained control authority')
        for cid,spec in CONFIG['exercises'].items():
            if cid in AI_GOALS and not full:
                mutation("from app.server import save;from app.game import CATALOG,campaign;import app.server as s;r=campaign(s);c=next(c for c in CATALOG['challenges'] if c['id']=="+repr(cid)+");save('game_award',{'run_id':r['id'],'challenge_id':c['id'],'xp':c['xp'],'test_fixture':True})")
                report['fixtures'].append(cid+' award only; AI not executed');continue
            assert base.api('/api/game')['current']==cid
            for action in ACTIONS.get(cid,[]):command(action)
            boot=base.api('/api/bootstrap');episode=boot['continuation']['episode']
            rows=[r for r in boot['records']['lab_event'] if r.get('campaign')==run and r.get('episode')==episode]
            answer={f['key']:f.get('expected',f['options'][0][0] if f.get('options') else 'El hecho observado se limita al portal y la campaña. El dueño debe validar el efecto, aceptar el residual y conservar una contraprueba que permita reabrir el cierre.') for p in spec['pages'] for f in p['fields']}
            if spec.get('ai_purpose'):
                a=next(a for a in reversed(boot['records']['ai']) if a.get('game_run')==run and a.get('purpose')==spec['ai_purpose'])
                assert a['mode']=='live-local' and a['model_digest_verified'] and a['no_control_execution']
                assert 'tools' not in a['inference_request'] and a['inference_request']['options']['num_gpu']==0
                answer.update(claim=a['output']['summary'],verdict='correct',reason='PHP-618 delimita condiciones de OOM y PHP-SCOPE describe una regresión funcional. La versión del CLI candidato no acredita el proceso web activo ni demuestra RCE. Conservo revisión humana y prueba posterior.')
                report['inferences'].append({k:a[k] for k in ['id','purpose','model','model_digest','elapsed_seconds','validation_errors']})
            if cid=='php-inventario':
                assert 'PHP 8.4.27' in next(r for r in rows if r['kind']=='php-cli')['body']['stdout']
                assert next(r for r in rows if r['kind']=='php-identity')['body']['version_id']==80426
            if cid=='ops-interrupcion':assert rows[-1]['status']==503
            if cid=='ops-metricas':answer['drifts']=str(boot['continuation']['metrics']['drift_events']);assert answer['drifts']=='1'
            if cid=='cierre-mapeo':answer.update(likelihood='2',operation='5',people='2',data='4',finance='3',index='40')
            payload={'challenge_id':cid,'answers':answer,'evidence_ids':[r['id'] for r in rows][-30:]}
            if cid=='encargo-ia':
                try:base.api('/api/advanced/record',{**payload,'evidence_ids':['PHP-EV-forged']})
                except HTTPError as exc:assert exc.code==400
                else:raise AssertionError('Forged evidence accepted')
            if cid=='ops-copia':
                base.dc('--profile','php','restart','php-legacy','php-patched')
                for _ in range(30):
                    health=base.dc('--profile','php','ps','--format','json','php-patched')
                    if 'healthy' in health:break
                    time.sleep(.5)
                report['copy_survives_php_restart']=True
            base.api('/api/advanced/record',payload);result=base.credit(cid)
            before=result['xp'];assert base.api('/api/game/verify',{})['xp']==before
            report['real_goals'].append(cid)
        command('cierre-exportar')
        bundle=json.loads(base.station('ssh','appdesk','cat ~/evidence/cierre-exportar.json'))
        boot=base.api('/api/bootstrap');export=next(r for r in reversed(boot['records']['lab_event']) if r.get('campaign')==run and r['kind']=='closure-export')
        assert export['sha256']==hashlib.sha256(canonical(bundle)).hexdigest()
        assert len(bundle['analysis'])==len(report['real_goals'])
        state=boot['continuation']['metrics'];assert state['restores_observed']==1 and state['drift_events']==1 and state['function_currently_proved']
        report.update(metrics=state,event_count=len(bundle['events']),dossier_sha256=export['sha256'],analysis_count=len(bundle['analysis']))
        if full:assert len(report['real_goals'])==24 and len(report['inferences'])==3
        (ROOT/'artifacts').mkdir(exist_ok=True)
        (ROOT/'artifacts'/('validation-continuation-full.json' if full else 'validation-continuation-ci.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print('PASS real goals:',len(report['real_goals']),'local inferences:',len(report['inferences']),'events:',report['event_count'],flush=True)
    finally:
        mutation('from app.server import save;save("game_campaign",'+repr(original)+')')
        print('Previous campaign restored; validation history preserved.',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');main(p.parse_args().full)
