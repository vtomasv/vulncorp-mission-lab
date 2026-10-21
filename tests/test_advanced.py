"""Boundary tests: clocks, causal controls, forged sources and truthful scope."""
import tempfile
import time
import unittest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from app import advanced, game, server


class Deadlines(unittest.TestCase):
    def test_final_uses_actual_early_alert_not_knowledge_or_update(self):
        result = advanced.deadline('2026-10-21T12:00:00Z','2026-10-21T14:00:00Z',True,True)
        self.assertEqual(result['early_due'],'2026-10-21T15:00:00Z')
        self.assertEqual(result['update_due'],'2026-10-22T12:00:00Z')
        self.assertEqual(result['final_due'],'2026-11-05T14:00:00Z')
        self.assertEqual(result['action_due'],'2026-10-28T12:00:00Z')
    def test_24h_requires_both_oiv_and_essential_function_affected(self):
        for oiv,affected in [(False,False),(False,True),(True,False)]:
            r=advanced.deadline('2026-10-21T12:00:00Z','2026-10-21T14:00:00Z',oiv,affected)
            self.assertEqual(r['update_due'],'2026-10-24T12:00:00Z')
    def test_ongoing_status_then_managed_final_and_timezone_equivalence(self):
        r=advanced.deadline('2026-10-21T09:00:00-03:00','2026-10-21T11:00:00-03:00',True,True,True,'2026-11-07T16:00:00Z')
        self.assertEqual(r['final_kind'],'status')
        self.assertEqual(r['managed_final_due'],'2026-11-22T16:00:00Z')
    def test_reject_ambiguous_or_impossible_clock(self):
        for known,early in [('2026-10-21T12:00:00','2026-10-21T14:00:00Z'),('2026-10-21T12:00:00Z','2026-10-21T16:00:00Z'),('2026-10-21T12:00:00Z','2026-10-21T11:00:00Z')]:
            with self.assertRaises(ValueError):advanced.deadline(known,early,True,True)


class EvidenceBoundary(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.old=server.DB;server.DB=Path(self.temp.name)/'lab.db'
        self.run=game.campaign(server);self.state={'campaign':self.run['id'],'episode':'EP-test','authz_fixed':False,'revoked':False}
        self.mock=patch('app.advanced.range_state',return_value=self.state);self.mock.start()
        for c in game.CATALOG['challenges'][:15]:
            server.save('game_award',{'run_id':self.run['id'],'challenge_id':c['id'],'xp':c['xp']})
    def tearDown(self):self.mock.stop();server.DB=self.old;self.temp.cleanup()
    def event(self,**kw):
        return server.save('lab_event',{'id':'RNG-'+str(time.time_ns()),'campaign':self.run['id'],'episode':'EP-test','occurred_at':time.time(),
            'actor':'appdesk','kind':'document','route':'/live/documents/SALUD-001','identity':'training-agua-user','status':200,
            'correlation':'TEST-one','authz_fixed':False,'revoked':False,**kw})
    def checks(self,id):return advanced.conditions(server,{'id':id},self.run)
    def payload(self,id):
        answers={f['key']:f.get('expected','Una conclusión de entrenamiento que identifica el alcance y reconoce los límites de la evidencia.') for p in advanced.CONFIG['exercises'][id]['pages'] for f in p['fields']}
        return {'challenge_id':id,'answers':answers,'evidence_ids':[]}
    def activate(self,id):
        for c in game.CATALOG['challenges'][15:]:
            if c['id']==id:break
            server.save('game_award',{'run_id':self.run['id'],'challenge_id':c['id'],'xp':c['xp']})
    def test_cannot_skip_or_overwrite_records_with_browser_id(self):
        with self.assertRaises(ValueError):advanced.record(server,self.payload('callback'))
        payload=self.payload('alcance');payload['id']=self.run['id']
        row=advanced.record(server,payload)
        self.assertNotEqual(row['id'],self.run['id'])
    def test_old_episode_and_other_campaign_do_not_count(self):
        for kw in [{'episode':'EP-old'},{'campaign':'OTHER'},{'occurred_at':self.run['started']-1}]:self.event(**kw)
        self.assertEqual(advanced.evidence(server,self.run,self.state),[])
    def test_forged_or_historical_sources_rejected(self):
        self.activate('callback');self.event(episode='EP-old',id='RNG-old')
        for ref in ['invented','RNG-old']:
            p=self.payload('callback');p['evidence_ids']=[ref]
            with self.assertRaises(ValueError):advanced.record(server,p)
    def test_browser_conclusion_does_not_replace_callback_receipt(self):
        self.activate('callback');e=self.event()
        p=self.payload('callback');p['evidence_ids']=[e['id']];advanced.record(server,p)
        self.assertFalse(all(r['ok'] for r in self.checks('callback')))
    def test_callback_receipt_must_reference_same_request_and_correlation(self):
        q=self.event(kind='request',route='/rig/callback',correlation='one')
        self.event(kind='collector',parent=q['id'],correlation='different')
        self.assertFalse(self.checks('callback')[2]['ok'])
        self.event(kind='collector',parent=q['id'],correlation='one')
        self.assertTrue(self.checks('callback')[2]['ok'])
    def test_mapping_needs_distinct_actual_behaviors_not_any_http_200(self):
        self.activate('mapeo');e=self.event(document_tenant='salud',correlation='SIM-one')
        p=self.payload('mapeo');p['answers'].update(t1190=e['id'],t1078=e['id']);p['evidence_ids']=[e['id']]
        with self.assertRaises(ValueError):advanced.record(server,p)
        b=self.event(identity='training-stolen-salud',correlation='SIM-two');p['answers']['t1078']=b['id'];p['evidence_ids'].append(b['id'])
        self.assertIn('id',advanced.record(server,p))
    def test_denial_without_legitimate_function_and_causal_order_is_insufficient(self):
        self.event(authz_fixed=True,status=403)
        self.assertFalse(all(r['ok'] for r in self.checks('autorizacion')))
        change=self.event(kind='control',action='fix')
        for identity,status in [('training-agua-user',403),('training-salud-user',200),('training-stolen-salud',200)]:
            self.event(identity=identity,status=status,authz_fixed=True)
        self.state['authz_fixed']=True
        checks=self.checks('autorizacion')
        self.assertFalse(next(c for c in checks if 'antes' in c['label'])['ok'])
        self.assertTrue(all(c['ok'] for c in checks if c['label'].startswith('Después:')))
    def test_every_added_goal_has_a_verified_condition_and_form(self):
        self.assertEqual(len(advanced.IDS),18)
        for id in advanced.IDS:
            self.assertTrue(self.checks(id))
            self.assertEqual(game.CHALLENGES[id]['form'],'advanced')


class RangePersistence(unittest.TestCase):
    def test_control_episode_and_sequence_survive_a_new_process(self):
        with tempfile.TemporaryDirectory() as folder:
            import os
            env={**os.environ,'LAB_RANGE_STATE':folder+'/validation.json'}
            subprocess.run([sys.executable,'-c',"from app import range_target as r;r.STATE.update(campaign='campaign-test',episode='EP-persist',authz_fixed=True);r.event('control',action='fix')"],env=env,check=True,capture_output=True)
            output=subprocess.run([sys.executable,'-c',"from app import range_target as r;assert r.STATE['authz_fixed'];assert r.STATE['episode']=='EP-persist';assert r.EVENTS[0]['kind']=='control';assert r.event('probe')['sequence']==2;print('persisted')"],env=env,check=True,capture_output=True,text=True)
            self.assertEqual(output.stdout.strip(),'persisted')


if __name__=='__main__':unittest.main()
