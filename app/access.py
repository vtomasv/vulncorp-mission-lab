"""Student connection details. The only downloadable private key is deliberately PUBLIC training data."""
import base64
import hashlib
import os
from pathlib import Path
from .game import verified_envelope
from .secure import secret

KEY_NAME='vulncorp_student_ed25519'
KEY_ROOT=Path(__file__).resolve().parents[1]/'training/ssh'
DOWNLOADS={f'/training/ssh/{name}':name for name in [KEY_NAME,KEY_NAME+'.pub']}

def fingerprint(public_key):
    fields=public_key.split()
    if len(fields)<2 or fields[0]!='ssh-ed25519':raise ValueError('Se esperaba una llave pública Ed25519.')
    blob=base64.b64decode(fields[1],validate=True)
    return 'SHA256:'+base64.b64encode(hashlib.sha256(blob).digest()).decode().rstrip('=')

def metadata(store):
    port=int(os.environ.get('LAB_SSH_PORT','2222'))
    if not 1<=port<=65535:raise ValueError('LAB_SSH_PORT debe ser un puerto válido.')
    result=store.request_target('http://workstation:9091/identity',headers={'X-Station-Key':secret('analyst')})
    envelope=result.get('body',{})
    host_key=envelope.get('event',{}).get('ssh_host_key') if result['status']==200 and verified_envelope(envelope,'analyst') else None
    public_key=(KEY_ROOT/(KEY_NAME+'.pub')).read_text().strip()
    return {'host':'127.0.0.1','port':port,'username':'student','authentication':'publickey','password':None,
        'key_passphrase_required':False,'training_key_public':True,'public_key':public_key,
        'key_fingerprint':fingerprint(public_key),'host_public_key':host_key,
        'host_fingerprint':fingerprint(host_key) if host_key else None,
        'private_key_url':f'/training/ssh/{KEY_NAME}','public_key_url':f'/training/ssh/{KEY_NAME}.pub',
        'mac_linux_command':'./lab.sh ssh','powershell_command':'.\\lab.ps1 ssh',
        'direct_command':f'ssh -i training/ssh/{KEY_NAME} -o IdentitiesOnly=yes -p {port} student@127.0.0.1',
        'scope':'Llave pública de entrenamiento: solo para esta instalación local. Los secretos de verificación y llaves internas no se publican.'}

def serve_key(handler,path):
    # Exact allowlist: this is never a filesystem browser or a secret-file endpoint.
    name=DOWNLOADS[path];raw=(KEY_ROOT/name).read_bytes()
    handler.send_response(200)
    handler.send_header('Content-Type','text/plain; charset=utf-8')
    handler.send_header('Content-Disposition',f'attachment; filename="{name}"')
    handler.send_header('Cache-Control','no-store')
    handler.send_header('X-Content-Type-Options','nosniff')
    handler.send_header('Content-Length',str(len(raw)))
    handler.end_headers();handler.wfile.write(raw)
