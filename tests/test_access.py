"""Only the deliberately public training pair is downloadable; station identity is authenticated."""
import base64
import hashlib
import hmac
import io
import os
import unittest
from unittest.mock import patch
from app import access,game,server

class AccessTests(unittest.TestCase):
    def setUp(self):self.public=(access.KEY_ROOT/(access.KEY_NAME+'.pub')).read_text().strip()
    def signed(self):
        event={'id':'station-identity','station':'analyst','ssh_host_key':self.public}
        return {'event':event,'signature':hmac.new(b'access-test',game.canonical(event),hashlib.sha256).hexdigest()}
    def metadata(self,response):
        with patch('app.access.secret',return_value='access-test'),patch('app.game.secret',return_value='access-test'),patch('app.server.request_target',return_value=response):return access.metadata(server)
    def test_access_has_key_auth_no_password_and_matches_custom_port(self):
        with patch.dict(os.environ,{'LAB_SSH_PORT':'2244'}):value=self.metadata({'status':200,'body':self.signed()})
        self.assertEqual(value['port'],2244);self.assertIsNone(value['password'])
        self.assertEqual(value['username'],'student');self.assertEqual(value['authentication'],'publickey')
        self.assertTrue(value['training_key_public']);self.assertIn('-p 2244',value['direct_command'])
        self.assertEqual(value['host_fingerprint'],access.fingerprint(self.public))
    def test_forged_station_cannot_supply_host_fingerprint(self):
        forged=self.signed();forged['signature']='incorrect'
        self.assertIsNone(self.metadata({'status':200,'body':forged})['host_fingerprint'])
    def test_unavailable_station_keeps_training_credentials_visible(self):
        result=self.metadata({'status':0,'body':{'error':'offline'}})
        self.assertIsNone(result['host_public_key']);self.assertEqual(result['public_key'],self.public)
    def test_only_intentionally_public_pair_is_downloadable(self):
        self.assertEqual(set(access.DOWNLOADS.values()),{access.KEY_NAME,access.KEY_NAME+'.pub'})
        self.assertNotIn('/training/ssh/../../secrets/control.key',access.DOWNLOADS)
        class Handler:
            def __init__(self):self.wfile=io.BytesIO();self.headers={}
            def send_response(self,status):self.status=status
            def send_header(self,name,value):self.headers[name]=value
            def end_headers(self):pass
        handler=Handler();access.serve_key(handler,'/training/ssh/'+access.KEY_NAME)
        self.assertEqual(handler.status,200);self.assertIn('attachment;',handler.headers['Content-Disposition'])
        self.assertEqual(handler.wfile.getvalue(),(access.KEY_ROOT/access.KEY_NAME).read_bytes())
    def test_public_fingerprint_uses_key_blob_not_comment(self):
        self.assertEqual(access.fingerprint(self.public),access.fingerprint(' '.join(self.public.split()[:2])+' another-comment'))
        expected='SHA256:'+base64.b64encode(hashlib.sha256(base64.b64decode(self.public.split()[1])).digest()).decode().rstrip('=')
        self.assertEqual(access.fingerprint(self.public),expected)
    def test_public_key_is_the_one_authorized_for_analysis_only(self):
        root=access.KEY_ROOT.parents[1]
        self.assertIn('/app/training/ssh/'+access.KEY_NAME+'.pub',(root/'stations/sshd-analyst.conf').read_text())
        self.assertNotIn('/training/',(root/'stations/sshd_config').read_text())

if __name__=='__main__':unittest.main()
