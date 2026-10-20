"""Verificación real del flujo local. Crea evidencia de prueba y restablece targets."""
import json
from urllib.request import Request,urlopen
from urllib.error import HTTPError

BASE='http://127.0.0.1:8000'
def call(path,data=None):
    req=Request(BASE+path,data=json.dumps(data).encode() if data else None,headers={'Content-Type':'application/json'})
    with urlopen(req,timeout=10) as r:return json.load(r)

def main():
    assert call('/health')['ok']
    assert len(call('/api/bootstrap')['clients'])==3
    call('/api/control',dict(action='reset',reason='Restablecimiento de targets para prueba de integración docente.'))
    try:
        assert call('/api/probe',{'action':'transaction'})['result']['body']['status']=='completed'
        assert call('/api/probe',{'action':'export'})['result']['status']==200
        control=call('/api/control',dict(action='restrict_export',reason='Prueba de restricción temporal, seguida de validación funcional.'))
        assert control['ok']
        assert call('/api/probe',{'action':'export'})['result']['status']==403
        assert call('/api/probe',{'action':'transaction'})['result']['body']['status']=='completed'
        assert call('/api/probe',{'action':'backup'})['result']['status']==200
        assert call('/api/control',dict(action='rotate_backup',reason='Rotación de una llave sintética para validar rechazo de la anterior.'))['ok']
        assert call('/api/probe',{'action':'backup'})['result']['status']==403
        from tests.test_core import decision
        result=call('/api/decisions',decision())
        assert result['calculation']['index']==64
        assert call('/api/export')['content_sha256']
        print('PASS: función real, acceso expuesto, mitigación, continuidad, rotación, riesgo y exportación.')
    finally:call('/api/control',dict(action='reset',reason='Limpieza final de la prueba integrada, preservando historial docente.'))

if __name__=='__main__':main()
