"""Validate the rendered Compose contract, including internal workstations and fixed management entry."""
import json
import sys
cfg=json.load(sys.stdin);services=cfg['services']
for role in ['mission','gateway','records','backup','workstation','ops','appdesk','validation','collector','webscan']:
    s=services[role]
    assert s['read_only'],role
    assert 'ALL' in s['cap_drop'],role
    assert not s.get('privileged',False),role
    assert s.get('network_mode')!='host',role
    assert not any('docker.sock' in str(v) for v in s.get('volumes',[])),role
for role in ['gateway','records','backup','workstation','ops','appdesk','validation','collector','webscan']:
    assert not services[role].get('ports'),role
    for net in services[role]['networks']:assert cfg['networks'][net]['internal'],(role,net)
for role,nets in {'workstation':{'edge'},'ops':{'edge','support'},'appdesk':{'edge','app'}}.items():
    assert set(services[role]['networks'])==nets,role
    assert set(services[role]['cap_add'])=={'CHOWN','DAC_OVERRIDE','FOWNER','SETUID','SETGID','SYS_CHROOT'} | {'AUDIT_WRITE'},role
for port in services['mission']['ports']:assert port['host_ip']=='127.0.0.1'
assert {p['target'] for p in services['mission']['ports']}=={8000,2222}
assert all(cfg['networks'][n]['internal'] for n in services['workstation']['networks'])
assert set(services['ollama']['networks'])=={'ai'} and cfg['networks']['ai']['internal']
assert not services['ollama'].get('ports')
assert services['init-game']['network_mode']=='none'
assert services['prepare-cache']['network_mode']=='none'
print('PASS: web y SSH de análisis en loopback; puestos y targets internos; redes distintas; IA interna; sin socket Docker ni privilegios generales.')

for role in ['validation','collector','webscan']:
    assert set(services[role]['networks'])=={'app'},role
assert '@sha256:' in services['webscan']['image']
assert int(services['webscan']['mem_limit'])==768*1024*1024
# Base stack + CPU model + on-demand ZAP stays below an 8 GiB VM budget.
active=['mission','gateway','records','backup','validation','collector','workstation','ops','appdesk','ollama','webscan']
assert sum(int(services[x]['mem_limit']) for x in active) < 8*1024**3
print('PASS: rango y ZAP internos, digest fijado y presupuesto de memoria <8 GiB.')
