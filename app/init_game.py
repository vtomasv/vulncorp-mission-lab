import os
import secrets
from pathlib import Path

root=Path(os.environ.get('LAB_SECRET_DIR','/secrets'))
root.mkdir(parents=True,exist_ok=True)
for name in ['control','analyst','ops','appdesk']:
    path=root/(name+'.key')
    if not path.exists():
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:f.write(secrets.token_hex(32)+'\n')
print('Claves del entorno preparadas. No se muestran ni se publican.')
