"""Progress must come from the right actor and campaign, once, with causal final proofs."""
import copy
import hashlib
import hmac
import io
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from app import game, server
from tests.test_core import decision

class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.old=server.DB;server.DB=Path(self.temp.name)/'game.db'
        self.run=game.campaign(server)
    def tearDown(self):server.DB=self.old;self.temp.cleanup()
    def station(self,action,role='analyst',result=None,when=None):
        return server.save('station',dict(action=action,station=role,result=result or {},occurred_at=when or time.time()))
    def observation(self,action,status=200,actor='analyst',body=None,when=None):
        return server.save('evidence',dict(action=action,actor=actor,result={'status':status,'body':body or {}},occurred_at=when or time.time()))
    def checks(self,id):return game.conditions(server,game.CHALLENGES[id],self.run,{})
    def complete(self,id):
        return server.save('game_award',{'id':'test-'+id,'run_id':self.run['id'],'challenge_id':id,'xp':game.CHALLENGES[id]['xp']})
    def test_no_click_or_written_decision_completes_first_goal(self):
        server.dispatch('/api/decisions',decision())
        with patch('app.game.collect',return_value={}):result=game.verify(server)
        self.assertEqual(result['xp'],0);self.assertEqual(result['current'],'contacto')
    def test_old_proof_cannot_complete_new_campaign(self):
        self.station('iniciar',result={'uid':1000},when=self.run['started']-5)
        self.assertFalse(self.checks('contacto')[0]['ok'])
    def test_later_scoped_proof_cannot_complete_resumed_older_campaign(self):
        server.save('station',{'action':'iniciar','station':'analyst','occurred_at':time.time(),
                               'game_run':'another-test-run','result':{'uid':1000}})
        self.assertFalse(self.checks('contacto')[0]['ok'])
    def test_session_interval_attributes_delayed_collection_to_actual_run(self):
        sessions=[{'run_id':'original','started':10},{'run_id':'test','started':20},{'run_id':'original','started':30}]
        self.assertEqual(game.proof_run(sessions,25),'test')
        self.assertEqual(game.proof_run(sessions,35),'original')
        self.assertIsNone(game.proof_run(sessions,5))
    def test_identity_and_role_are_required(self):
        self.station('iniciar','ops',{'uid':1000});self.station('iniciar',result={'uid':0})
        self.assertFalse(self.checks('contacto')[0]['ok'])
    def test_retry_is_idempotent_and_next_goal_stays_locked_without_proof(self):
        self.station('iniciar',result={'uid':1000})
        with patch('app.game.collect',return_value={}):
            for _ in range(4):result=game.verify(server)
        self.assertEqual(result['xp'],40);self.assertEqual(len(result['awards']),1)
        self.assertEqual(result['states']['funcion'],'active');self.assertEqual(result['states']['segmento'],'locked')
    def test_management_probe_does_not_count_as_workstation_observation(self):
        server.save('evidence',{'action':'transaction','result':{'status':200,'body':{'status':'completed'}},'occurred_at':time.time()})
        # Legacy records have no station actor; they remain exportable but cannot award game progress.
        self.assertFalse(self.checks('funcion')[0]['ok'])
    def test_status_200_without_business_completion_is_insufficient(self):
        self.observation('transaction',body={'status':'failed'})
        self.assertFalse(self.checks('funcion')[0]['ok'])
    def test_wrong_zone_cannot_complete_public_observation(self):
        self.observation('transaction',actor='appdesk',body={'status':'completed'})
        self.assertFalse(self.checks('funcion')[0]['ok'])
    def test_hmac_rejects_tampering_and_wrong_station(self):
        event={'id':'ST-test','station':'analyst','action':'iniciar','result':{'uid':1000}}
        signature=hmac.new(b'test-key',game.canonical(event),hashlib.sha256).hexdigest()
        envelope={'event':event,'signature':signature}
        with patch('app.game.secret',return_value='test-key'):
            self.assertTrue(game.verified_envelope(envelope,'analyst'))
            self.assertFalse(game.verified_envelope(envelope,'ops'))
            envelope['event']['result']['uid']=0
            self.assertFalse(game.verified_envelope(envelope,'analyst'))
    def test_collect_uses_signed_identity_for_every_interface(self):
        identity={'id':'station-identity','station':'analyst','addresses':['10.0.0.5','10.9.0.5']}
        signed={'event':identity,'signature':hmac.new(b'test-key',game.canonical(identity),hashlib.sha256).hexdigest()}
        def read(request,timeout):
            value={'identity':signed,'proofs':[]} if 'workstation' in request.full_url else {}
            return io.BytesIO(json.dumps(value).encode())
        events=[{'id':'NET-'+peer,'peer':peer,'path':'/catalog','status':200,'body':{},'occurred_at':time.time(),'boot_id':'test'} for peer in ['10.9.0.5','10.0.0.1']]
        def target(url,headers):return {'body':{'events':events if 'backup' in url else []}}
        with patch('app.game.secret',return_value='test-key'),patch('app.game.urlopen',side_effect=read),patch('app.server.request_target',side_effect=target):
            game.collect(server)
        rows=server.records('evidence')
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['actor'],'analyst')
        self.assertEqual(rows[0]['id'],'NET-10.9.0.5')

    def test_network_zone_requires_all_expected_results(self):
        self.station('red',result={'targets':[{'target':'gateway','result':'reachable'}]})
        self.assertFalse(self.checks('segmento')[0]['ok'])
    def test_catalogue_is_extensible_acyclic_and_xp_positive(self):
        seen=set();zones={z['id'] for z in game.CATALOG['zones']}
        for c in game.CATALOG['challenges']:
            self.assertTrue(set(c['requires'])<=seen);self.assertGreater(c['xp'],0)
            self.assertIn(c['zone'],zones);seen.add(c['id'])
        self.assertEqual(len(seen),len(game.CHALLENGES))
    def test_analysis_cannot_skip_prerequisites(self):
        with self.assertRaises(ValueError):game.analysis(server,{'challenge_id':'proveedor','reason':'Una explicación larga no reemplaza las pruebas del puesto.'})
    def test_analysis_cannot_replace_an_existing_record_by_supplied_id(self):
        for c in game.CATALOG['challenges']:
            if c['id']=='proveedor':break
            self.complete(c['id'])
        record=game.analysis(server,{'id':self.run['id'],'challenge_id':'proveedor','duplicate':'VENDOR-06','misattributed':'VENDOR-07','reason':'La evidencia de cada activo permite distinguir duplicación de atribución incorrecta.'})
        self.assertNotEqual(record['id'],self.run['id'])
        self.assertEqual(server.records('game_campaign')[0]['id'],self.run['id'])

    def test_two_contexts_must_link_observed_export_not_only_hypothesis(self):
        a=decision();server.dispatch('/api/decisions',a)
        b=copy.deepcopy(a);b['client_id']='agua';b['impacts']['operation']=2;server.dispatch('/api/decisions',b)
        self.assertFalse(self.checks('contexto')[0]['ok'])
        proof=self.observation('export')
        for d in [a,b]:d['evidence_ids']=[proof['id']];server.dispatch('/api/decisions',d)
        self.assertTrue(all(c['ok'] for c in self.checks('contexto')))
    def test_portfolio_without_committed_measure_is_not_enough(self):
        server.dispatch('/api/portfolio',{'client_id':'salud','packages':['B','C'],'reason':'Una alternativa viable, pero no contiene la medida comprometida.'})
        self.assertFalse(self.checks('cartera')[0]['ok'])
    def test_denial_alone_cannot_prove_continuity(self):
        self.station('proteger','appdesk',{'status':200})
        self.observation('export',403)
        with patch('app.server.request_target',return_value={'body':{'state':{'restrict_export':True}}}):checks=self.checks('continuidad')
        self.assertTrue(checks[0]['ok']);self.assertFalse(checks[1]['ok']);self.assertFalse(checks[3]['ok'])
    def test_final_requires_proofs_after_change_and_both_references(self):
        old=self.observation('transaction',body={'status':'completed'})
        self.station('proteger','appdesk',{'status':200})
        denied=self.observation('export',403)
        d=decision();d['state']='residual';d['evidence_ids']=[denied['id'],old['id']];server.dispatch('/api/decisions',d)
        with patch('app.server.request_target',return_value={'body':{'state':{'restrict_export':True}}}):
            self.assertFalse(self.checks('continuidad')[3]['ok'])
            business=self.observation('transaction',body={'status':'completed'})
            d['evidence_ids']=[denied['id'],business['id']];server.dispatch('/api/decisions',d)
            self.assertTrue(all(c['ok'] for c in self.checks('continuidad')))
        with patch('app.server.request_target',return_value={'body':{'state':{'restrict_export':False}}}):
            self.assertFalse(self.checks('continuidad')[2]['ok'])
    def test_new_campaign_does_not_inherit_old_awards(self):
        self.complete('contacto');server.save('game_campaign',{'started':time.time(),'catalog_version':'2.0'})
        self.assertEqual(game.snapshot(server)['xp'],0)

if __name__=='__main__':unittest.main()
