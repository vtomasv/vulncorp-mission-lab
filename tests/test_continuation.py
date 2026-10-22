"""Control/evidence boundary tests. All runtime/model responses here are mocks.
Real PHP and CPU inference are validated separately by integration_continuation.
"""
import hashlib
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from app import continuation as lab, game, server

class FinalBoundary(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.old=server.DB;server.DB=Path(self.temp.name)/'lab.db'
        self.run=game.campaign(server)
        for c in game.CATALOG['challenges'][:33]:self.award(c)
        self.s=lab.state(server,self.run)
        self.net=patch.object(lab,'target',return_value=(0,{}));self.net.start()
    def tearDown(self):self.net.stop();server.DB=self.old;self.temp.cleanup()
    def award(self,c):server.save('game_award',{'run_id':self.run['id'],'challenge_id':c['id'],'xp':c['xp'],'test_fixture':True})
    def activate(self,cid):
        for c in game.CATALOG['challenges'][33:]:
            if c['id']==cid:break
            self.award(c)
    def event(self,kind,**kw):return lab.emit(server,self.run,self.s,kind,**kw)
    def payload(self,cid,refs):
        answer={f['key']:f.get('expected',f['options'][0][0] if f.get('options') else 'Una observación acotada del caso, con responsable y una contraprueba que permite objetar el cierre profesional.') for p in lab.CONFIG['exercises'][cid]['pages'] for f in p['fields']}
        return {'challenge_id':cid,'answers':answer,'evidence_ids':refs}
    def test_24_goals_preserve_original_ids_and_have_real_checks(self):
        self.assertEqual(len(lab.IDS),24);self.assertEqual(len(game.CATALOG['challenges']),57)
        for cid in lab.IDS:self.assertTrue(lab.conditions(server,{'id':cid},self.run))
    def test_browser_cannot_run_operational_actions(self):
        with self.assertRaises(ValueError):server.dispatch('/api/continuation/action',{'action':'php-desplegar'})
    def test_changes_cannot_skip_active_goal_or_accept_an_arbitrary_command(self):
        for a in ['php-desplegar','ops-danar','ops-restaurar','ia-base','curl http://example.com',None,{}]:
            with self.assertRaises(ValueError):lab.execute(server,a)
    def test_only_current_campaign_episode_and_start_are_evidence(self):
        a=self.event('mission-open');self.event('mission-open',episode='old');self.event('mission-open',campaign='other');self.event('mission-open',occurred_at=self.run['started']-1)
        self.assertEqual([r['id'] for r in lab.rows(server,self.run,self.s)],[a['id']])
        for ref in ['forged','old']:
            with self.assertRaises(ValueError):lab.record(server,self.payload('encargo-ia',[ref]))
    def test_a_form_does_not_replace_execution(self):
        e=self.event('unrelated');lab.record(server,self.payload('encargo-ia',[e['id']]))
        self.assertFalse(all(r['ok'] for r in lab.conditions(server,{'id':'encargo-ia'},self.run)))
    def test_stale_success_does_not_close_after_a_new_revision(self):
        self.s.update(active='patched');lab.persist(server,self.s)
        e=self.event('php-document',status=200,body={'document':{'status':'completed'}})
        self.assertTrue(lab.functional(e));self.s['revision']+=1;lab.persist(server,self.s)
        self.assertFalse(lab.current_proof(lab.rows(server,self.run,self.s),self.s,'php-document'))
    def test_deploy_requires_the_real_expected_version_and_digest(self):
        self.activate('php-despliegue');lab.persist(server,self.s,multipart_blocked=True)
        for body in [{'version_id':80427,'base_digest':'wrong'},{'version_id':80426,'base_digest':lab.IMAGES['patched']['digest']}]:
            with patch.object(lab,'target',return_value=(200,body)):
                with self.assertRaises(ValueError):lab.execute(server,'php-desplegar')
        self.assertEqual(lab.state(server,self.run)['active'],'legacy')
    def test_restore_does_not_accept_a_different_document_hash(self):
        self.activate('ops-restauracion');lab.persist(server,self.s,active='patched',interrupted=True,copy_sha256='expected')
        self.event('php-document',status=503)
        with patch.object(lab,'target',return_value=(200,{'document_sha256':'different'})):
            with self.assertRaises(ValueError):lab.execute(server,'ops-restaurar')
        self.assertTrue(lab.state(server,self.run)['interrupted'])
    def test_risk_arithmetic_is_checked_but_owner_vector_is_explicit(self):
        self.activate('cierre-mapeo');e=self.event('closure-case');p=self.payload('cierre-mapeo',[e['id']]);p['answers'].update(likelihood='3',operation='4',people='2',data='3',finance='2',index='12')
        with self.assertRaises(ValueError):lab.record(server,p)
        p['answers']['index']='48';self.assertIn('id',lab.record(server,p))
    def test_repeated_http_observations_are_not_extra_drift_events(self):
        self.event('ops-drift')
        for _ in range(5):self.event('php-identity',body={'deployment':'container-a'})
        m=lab.metrics(lab.rows(server,self.run,self.s),self.s)
        self.assertEqual(m['drift_events'],1);self.assertEqual(m['deployments_verified'],1)
    def test_final_ai_receives_current_owner_and_observation_without_tools(self):
        e=self.event('php-document',status=200,body={'document':{'status':'completed'}})
        def response(client,question,findings,documents):
            self.assertIn('ArchivoSur',question)
            self.assertEqual({d['id'] for d in documents},{'PHP-618','PHP-619','PHP-RELEASE','PHP-SCOPE','PHP-ENCARGO','PHP-CLIENTE',e['id']})
            return {'inference_request':{},'source_ids':[d['id'] for d in documents]}
        with patch('app.ai.propose',side_effect=response):
            a=lab.ai_run(server,self.run,self.s,'php-ai-final')
        self.assertTrue(a['no_control_execution'])

    def test_export_hash_covers_bundle_and_can_be_refreshed_after_completion(self):
        for c in game.CATALOG['challenges'][33:]:self.award(c)
        result=lab.execute(server,'cierre-exportar')
        self.assertEqual(result['sha256'],hashlib.sha256(lab.canonical(result['bundle'])).hexdigest())
        self.assertEqual(result['bundle']['graded_exam'],False)
        self.assertEqual(lab.state(server,self.run)['episode'],self.s['episode'])

if __name__=='__main__':unittest.main()
