"""Native client auth, real downloaded training pair, host identity and fixed-entry boundaries."""
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
from app.access import fingerprint

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8095'

def command(args):return subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=20)

def main():
    with urlopen(BASE+'/api/access') as r:access=json.load(r)
    assert access['username']=='student' and access['password'] is None
    assert access['host_fingerprint'] and access['training_key_public']
    with tempfile.TemporaryDirectory() as folder:
        folder=Path(folder);private=folder/'training';public=folder/'training.pub';known=folder/'known_hosts'
        for path,url in [(private,access['private_key_url']),(public,access['public_key_url'])]:
            with urlopen(BASE+url) as response:
                assert 'attachment' in response.headers['Content-Disposition'];path.write_bytes(response.read())
        private.chmod(0o600)
        derived=command(['ssh-keygen','-y','-f',str(private)])
        assert derived.returncode==0 and derived.stdout.split()[:2]==public.read_text().split()[:2]
        assert fingerprint(derived.stdout)==access['key_fingerprint']
        assert fingerprint(access['host_public_key'])==access['host_fingerprint']
        known.write_text(f"[127.0.0.1]:{access['port']} {access['host_public_key']}\n")
        options=['-p',str(access['port']),'-i',str(private),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','ConnectTimeout=5',
                 '-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known)]
        result=command(['ssh',*options,'student@127.0.0.1','id'])
        assert result.returncode==0 and 'uid=1000(student)' in result.stdout,result.stderr
        interactive=command(['ssh',*options,'-tt','student@127.0.0.1','id'])
        assert interactive.returncode==0 and 'uid=1000(student)' in interactive.stdout,interactive.stderr
        for denied in [
            ['ssh',*options,'root@127.0.0.1','id'],
            ['ssh',*options,'-o','PubkeyAuthentication=no','student@127.0.0.1','id'],
            ['ssh',*options,'-W','gateway:8080','student@127.0.0.1'],
        ]:
            result=command(denied);assert result.returncode!=0,(denied,result.stdout)
        other=folder/'unrelated'
        assert command(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(other)]).returncode==0
        other_options=options.copy();other_options[other_options.index(str(private))]=str(other)
        assert command(['ssh',*other_options,'student@127.0.0.1','id']).returncode!=0
    for url in ['/training/ssh/control.key','/training/ssh/host_ed25519','/training/ssh/..%2f..%2fsecrets/control.key']:
        try:urlopen(BASE+url);raise AssertionError('Unlisted key path was served: '+url)
        except HTTPError as exc:assert exc.code==404
    print('PASS: downloaded training key; pinned host fingerprint; UID 1000; root/password/wrong-key/forwarding denied; private internal paths unavailable.')

if __name__=='__main__':main()
