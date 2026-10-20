"""Comprueba el contrato de aislamiento del Compose renderizado, desde stdin."""
import json
import sys

cfg=json.load(sys.stdin)
services=cfg['services']
for role in ['mission','gateway','records','backup']:
    s=services[role]
    assert s['read_only'],role
    assert 'ALL' in s['cap_drop'],role
    assert not s.get('privileged',False),role
    assert s.get('network_mode')!='host',role
    assert not any('docker.sock' in str(v) for v in s.get('volumes',[])),role
for role in ['gateway','records','backup']:
    assert not services[role].get('ports'),role
    for net in services[role]['networks']:assert cfg['networks'][net]['internal'],(role,net)
for port in services['mission']['ports']:assert port['host_ip']=='127.0.0.1'
assert set(services['ollama']['networks'])=={'ai'}
assert cfg['networks']['ai']['internal']
assert not services['ollama'].get('ports')
print('PASS: publicación loopback, targets internos, IA interna, capacidades y montajes acotados.')
