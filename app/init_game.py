import os
import secrets
from pathlib import Path

root=Path(os.environ.get('LAB_SECRET_DIR','/secrets'))
root.mkdir(parents=True,exist_ok=True)
for name in ['control','analyst','ops','appdesk','php']:
    path=root/(name+'.key')
    if not path.exists():
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:f.write(secrets.token_hex(32)+'\n')
print('Claves del entorno preparadas. No se muestran ni se publican.')

# PHP receives only its own key, never workstation/control identities.
if Path("/php-secret").exists():
    Path("/php-secret/runtime.key").write_text((root/"php.key").read_text())
    Path("/php-secret/runtime.key").chmod(0o600)
if Path("/php-data").exists():
    Path("/php-data").chmod(0o700)
