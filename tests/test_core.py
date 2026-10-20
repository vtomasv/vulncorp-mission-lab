import copy
import hashlib
import json
import tempfile
import io
import unittest
from pathlib import Path
from unittest.mock import patch
from app import risk, ai, server
from app.fixtures import CLIENTS,FINDINGS,CORPUS


def decision():
    return {'client_id':'salud','finding_id':'F-02','state':'inherent','likelihood':4,
            'impacts':dict(operation=4,people=3,data=4,financial=3),
            'ssvc':dict(exploitation='P',exposure='O',automatable='Y',human_impact='H'),
            'reason':'La API sostiene resultados urgentes; debo comprobar la ruta y consultar al dueño.',
            'owner':'Dueño de entrenamiento','evidence_ids':['EV-EXPORT']}


class RiskTests(unittest.TestCase):
    def test_context_changes_order(self):
        expected={'salud':[8,64,60,36],'agua':[4,32,60,48],'digital':[8,80,24,48]}
        for client in CLIENTS:
            actual=[]
            for f in FINDINGS[:4]:
                impacts=dict(zip(['operation','people','data','financial'],client['impacts'][f['id']]))
                actual.append(risk.score(f['likelihood'],impacts)['index'])
            self.assertEqual(actual,expected[client['id']])

    def test_max_impact_preserves_people(self):
        self.assertEqual(risk.score(3,dict(operation=1,people=5,data=1,financial=1))['index'],60)

    def test_reject_float_bool_out_of_range(self):
        for level in [0,6,True,1.5,'4',None]:
            with self.assertRaises(ValueError):risk.score(level,dict(operation=1,people=1,data=1,financial=1))

    def test_all_72_official_branches(self):
        self.assertEqual(len(risk.TREE['mapping']),72)
        seen=set()
        for row in risk.TREE['mapping']:
            vals={key:row[field] for key,field in risk.INPUTS.items()}
            seen.add(tuple(vals.values()))
            self.assertEqual(risk.ssvc(vals)['outcome'],risk.OUTCOMES[row[risk.TREE['outcome']]])
        self.assertEqual(len(seen),72)

    def test_human_impact_changes_urgency(self):
        vals=dict(exploitation='A',exposure='O',automatable='Y',human_impact='H')
        self.assertEqual(risk.ssvc(vals)['outcome'],'Immediate')
        vals['human_impact']='L'
        self.assertEqual(risk.ssvc(vals)['outcome'],'Out-of-Cycle')

    def test_reject_cisa_labels_and_missing_inputs(self):
        with self.assertRaises(ValueError):risk.ssvc({'exploitation':'Act'})
        with self.assertRaises(ValueError):risk.ssvc(dict(exploitation='A',exposure='O',automatable='Y',human_impact='5'))


class AITests(unittest.TestCase):
    def valid(self):return dict(summary='Propuesta',facts=[dict(statement='Hipótesis',evidence_ids=['EV-EXPORT'])],missing_context=['Dueño'],options=['Restringir'],limitations=['Falta prueba'])
    def test_reference_validation(self):
        self.assertEqual(ai.validate(self.valid(),{'EV-EXPORT'}),[])
        self.assertTrue(ai.validate(self.valid(),{'EV-RISK'}))
    def test_reject_malformed_facts(self):
        value=self.valid();value['facts']=['confía en mí']
        self.assertTrue(ai.validate(value,{'EV-EXPORT'}))
    def test_retrieval_is_bounded_and_traceable(self):
        docs,findings=ai.retrieve('priorizar exportación',['F-02'])
        self.assertEqual(len(docs),4)
        self.assertIn('EV-EXPORT',{d['id'] for d in docs})
        self.assertEqual(findings[0]['id'],'F-02')
    def test_schema_does_not_grant_actions(self):
        self.assertNotIn('tools',ai.SCHEMA)
        self.assertNotIn('risk',ai.SCHEMA['properties'])
    def test_reference_model_digest_cannot_change_silently(self):
        for digest,available in [(ai.MODEL_LOCK['digest'],True),('changed',False)]:
            response=io.BytesIO(json.dumps({'models':[{'name':ai.MODEL_LOCK['model'],'digest':digest}]}).encode())
            with patch('app.ai.MODEL',ai.MODEL_LOCK['model']),patch('app.ai.urlopen',return_value=response):
                self.assertEqual(ai.status()['available'],available)
    def test_audit_preserves_actual_question_and_request(self):
        response=io.BytesIO(json.dumps({'message':{'content':json.dumps(self.valid())}}).encode())
        with patch('app.ai.status',return_value={'available':True,'digest':'tested','digest_verified':True}),patch('app.ai.urlopen',return_value=response):
            result=ai.propose('salud','¿Qué evidencia falta verificar?',['F-02'])
        self.assertEqual(result['question'],'¿Qué evidencia falta verificar?')
        self.assertEqual(result['inference_request']['options']['num_gpu'],0)
        self.assertIn(result['question'],result['inference_request']['messages'][1]['content'])


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.previous=server.DB;server.DB=Path(self.temp.name)/'test.db'
    def tearDown(self):server.DB=self.previous;self.temp.cleanup()
    def test_decisions_append_and_survive_reopen(self):
        a=server.dispatch('/api/decisions',decision());b=server.dispatch('/api/decisions',decision())
        self.assertNotEqual(a['id'],b['id']);self.assertEqual(a['calculation']['index'],64)
        self.assertEqual(len(server.records('decision')),2)
    def test_reject_invented_evidence_and_short_reason(self):
        data=decision();data['evidence_ids']=['EV-FAKE']
        with self.assertRaises(ValueError):server.dispatch('/api/decisions',data)
        data=decision();data['reason']='porque sí'
        with self.assertRaises(ValueError):server.dispatch('/api/decisions',data)
    def test_reject_duplicate_as_independent_risk(self):
        data=decision();data['finding_id']='VENDOR-06'
        with self.assertRaises(ValueError):server.dispatch('/api/decisions',data)
    def test_controls_are_whitelisted(self):
        with self.assertRaises(ValueError):server.dispatch('/api/control',{'action':'exec','reason':'Una razón suficientemente larga para probar límites.'})
    def test_probe_denial_is_evidence_not_success(self):
        with patch('app.server.request_target',return_value={'status':0,'body':{'error':'offline'},'elapsed_ms':1}):
            result=server.dispatch('/api/probe',{'action':'export'})
        self.assertEqual(result['result']['status'],0)
        self.assertTrue(result['observed'])
    def test_portfolio_rejects_budget_and_duplicates(self):
        for packs in [['D'],['A','B','C'],['A','A']]:
            with self.assertRaises(ValueError):server.dispatch('/api/portfolio',{'client_id':'salud','packages':packs,'reason':'Tratamiento justificado por la continuidad del servicio.'})
    def test_portfolio_accepts_valid_costs(self):
        r=server.dispatch('/api/portfolio',{'client_id':'salud','packages':['A','B'],'reason':'Priorizar el servicio y la recuperación, con ventanas compatibles.'})
        self.assertEqual((r['engineering_hours'],r['downtime_minutes']),(4,10))
    def test_formative_note_requires_reflection(self):
        with self.assertRaises(ValueError):server.dispatch('/api/notes',{'task_id':'1-1','answer':'listo'})
        r=server.dispatch('/api/notes',{'task_id':'1-1','answer':'Observé una transacción; esto solo demuestra función, no seguridad.'})
        self.assertIsNone(r['grade']);self.assertTrue(r['formative'])
    def test_cannot_accept_invalid_ai_output(self):
        record=server.save('ai',{'validation_errors':['Referencia falsa']})
        with self.assertRaises(ValueError):server.dispatch('/api/ai/review',{'audit_id':record['id'],'verdict':'accept','reason':'Esta razón no convierte una referencia inventada en evidencia real.'})
    def test_export_hash(self):
        server.dispatch('/api/decisions',decision());bundle=server.export_bundle();digest=bundle.pop('content_sha256')
        self.assertEqual(hashlib.sha256(json.dumps(bundle,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),digest)
    def test_context_reopens_reasoning_not_old_scores(self):
        before=server.dispatch('/api/decisions',decision())
        server.dispatch('/api/inject',{'client_id':'salud'})
        self.assertEqual(server.records('decision')[0]['calculation'],before['calculation'])
        self.assertEqual(len(server.records('context')),1)
    def test_scan_import_keeps_actual_and_curated_apart(self):
        r=server.dispatch('/api/scan/import',{'report':{'matches':[{'artifact':{'name':'Django','version':'3.2'},'vulnerability':{'id':'CVE-2021-35042','severity':'Critical'}}]}})
        self.assertEqual(r['matches_total'],1);self.assertEqual(len(FINDINGS),7)
    def test_grype_alias_preserves_ghsa_and_cve(self):
        report={'matches':[{'artifact':{'name':'requests','version':'2.31.0'},
            'vulnerability':{'id':'GHSA-9wx4-h78v-vm56','severity':'Medium'},
            'relatedVulnerabilities':[{'id':'CVE-2024-35195'}]}]}
        result=server.dispatch('/api/scan/import',{'report':report})['legacy_matches'][0]
        self.assertEqual(result['id'],'GHSA-9wx4-h78v-vm56')
        self.assertEqual(result['cve'],'CVE-2024-35195')


if __name__=='__main__':unittest.main()
