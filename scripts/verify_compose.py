"""Validate the rendered Compose contract, including internal workstations and fixed management entry."""
import json
import sys
cfg=json.load(sys.stdin);services=cfg['services']
for role in ['mission','gateway','records','backup','workstation','ops','appdesk']:
    s=services[role]
    assert s['read_only'],role
    assert 'ALL' in s['cap_drop'],role
    assert not s.get('privileged',False),role
    assert s.get('network_mode')!='host',role
    assert not any('docker.sock' in str(v) for v in s.get('volumes',[])),role
for role in ['gateway','records','backup','workstation','ops','appdesk']:
    assert not services[role].get('ports'),role
    for net in services[role]['networks']:assert cfg['networks'][net]['internal'],(role,net)
for role,nets in {'workstation':{'edge'},'ops':{'edge','support'},'appdesk':{'edge','app'}}.items():
    assert set(services[role]['networks'])==nets,role
    assert set(services[role]['cap_add'])=={'CHOWN','DAC_OVERRIDE','FOWNER','SETUID','SETGID','SYS_CHROOT'} | ({'AUDIT_WRITE'} if role!='workstation' else set()),role
for port in services['mission']['ports']:assert port['host_ip']=='127.0.0.1'
assert set(services['ollama']['networks'])=={'ai'} and cfg['networks']['ai']['internal']
assert not services['ollama'].get('ports')
assert services['init-game']['network_mode']=='none'
assert services['prepare-cache']['network_mode']=='none'
print('PASS: loopback único; puestos y targets internos; redes distintas; IA interna; sin socket Docker ni privilegios generales.')
