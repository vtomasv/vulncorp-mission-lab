"""Fixed workstation actions for the validation range, with genuine tool receipts."""
import hashlib
import json
import time
import uuid
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from .secure import secret

ACTIONS = {'abrir', 'callback', 'marcador', 'transferencia', 'zap', 'simular', 'cronologia',
           'ensayar', 'corregir', 'revocar', 'capa', 'incidente', 'ia-expediente'}


def execute(action, agent):
    from .advanced import CONFIG, canonical
    http = agent.http
    headers = {'X-Lab-Control': secret('control')}
    code, game = http('http://mission:8000/api/game')
    if code != 200: raise ValueError('El centro de misión no está disponible.')
    campaign = game['run']['id']
    if action == 'abrir':
        code, body = http('http://validation:8083/_control', {'action': 'open', 'campaign': campaign}, headers)
    else: code, body = http('http://validation:8083/_status', headers=headers)
    if code != 200 or body.get('state', {}).get('campaign') != campaign:
        raise ValueError('Ejecuta lab abrir desde aplicaciones para abrir este episodio. No se reinician los objetivos previos.')
    state = body['state']
    gates={'corregir':'autorizacion','revocar':'revocacion'}
    if action in gates and game.get('current')!=gates[action]:
        raise ValueError('Este cambio se habilita en su objetivo. Conserva primero la evidencia y el análisis anteriores.')
    result = {'campaign': campaign, 'episode': state['episode'], 'state': state}
    def request(route, token='', correlation=None):
        h = {'X-Correlation-ID': correlation or 'MAN-' + uuid.uuid4().hex}
        if token: h['Authorization'] = 'Bearer ' + token
        status, value = http('http://gateway:8080/range' + route, headers=h)
        if status == 0 or status >= 500: raise ValueError('El rango no pudo completar la prueba.')
        return {'route': route, 'identity': token or 'anonymous', 'status': status, 'body': value}
    if action == 'abrir':
        result['scope'] = 'gateway:8080/range; validation:8083 y collector:8084 internos. Sin Internet ni datos reales.'
    elif action in ['callback', 'marcador']:
        result['observation'] = request('/rig/' + ('callback' if action == 'callback' else 'marker'))
    elif action == 'transferencia':
        result['observations'] = [request('/vuln/documents/SALUD-001', 'training-agua-user'),
                                  request('/fixed/documents/SALUD-001', 'training-agua-user'),
                                  request('/fixed/documents/SALUD-001', 'training-salud-user'),
                                  request('/fixed/documents/SALUD-001')]
    elif action in ['simular', 'ensayar']:
        prefix = ('SIM-' if action == 'simular' else 'TEST-') + uuid.uuid4().hex
        route = '/vuln' if action == 'simular' else '/live'
        tokens = ['training-agua-user', 'training-stolen-salud', ''] if action == 'simular' else ['training-agua-user', 'training-salud-user', 'training-stolen-salud']
        result['declared_simulation'] = True
        result['observations'] = [request(route + '/documents/SALUD-001', token, prefix + '-' + str(i)) for i, token in enumerate(tokens)]
        result['limit'] = 'Uso deliberado de una credencial sintética presentada como comprometida en el guion; no se ha demostrado robo de credenciales.'
    elif action in ['corregir', 'revocar']:
        code,audit=http('http://validation:8083/_audit',headers=headers)
        trials=[r for r in audit.get('events',[]) if r.get('episode')==state['episode'] and r.get('kind')=='document'
                and r.get('correlation','').startswith('TEST-') and not r.get('revoked')
                and r.get('authz_fixed')==(action=='revocar')]
        expected={'training-agua-user':403 if action=='revocar' else 200,'training-salud-user':200,'training-stolen-salud':200}
        if not all(any(r['identity']==token and r['status']==status for r in trials) for token,status in expected.items()):
            raise ValueError('Conserva primero las tres respuestas anteriores al cambio: ejecuta lab ensayar y revisa el resultado.')
        code, ack = http('http://validation:8083/_control', {'action': 'fix' if action == 'corregir' else 'revoke'}, headers)
        if code != 200: raise ValueError('El servicio no confirmó el cambio.')
        result['ack'] = ack
    elif action == 'cronologia':
        code, audit = http('http://validation:8083/_audit', headers=headers)
        if code != 200: raise ValueError('No se pudo obtener el registro del servicio.')
        rows = [r for r in audit['events'] if r.get('episode') == state['episode'] and r.get('correlation', '').startswith('SIM-') and r['kind'] == 'document'][-3:]
        result['events'] = rows
        result['file'] = agent.write_student('cronologia.json', rows)
    elif action == 'capa':
        code, layer = http('http://mission:8000/api/advanced/layer')
        if code != 200 or 'error' in layer: raise ValueError(layer.get('error', 'Capa no disponible.'))
        result['layer_sha256'] = hashlib.sha256(canonical(layer)).hexdigest()
        result['file'] = agent.write_student('attack-layer.json', layer)
        result['techniques'] = [t['techniqueID'] for t in layer['techniques']]
    elif action == 'incidente':
        result['dossier'] = CONFIG['incident']
        result['file'] = agent.write_student('incidente-oiv.json', CONFIG['incident'])
    elif action == 'ia-expediente':
        code, audit = http('http://mission:8000/api/advanced/ai', {}, timeout=250)
        if code != 200: raise ValueError(audit.get('error', 'Modelo no disponible.'))
        result.update(audit_id=audit['id'], model=audit['model'], live=audit['mode'] == 'live-local')
        result['file'] = agent.write_student('ia-expediente.json', audit)
        return result, json.dumps(audit, ensure_ascii=False, indent=2) + '\nRevisa afirmación, fuente y límites en el objetivo del juego.'
    elif action == 'zap':
        # Fixed four requests via a real passive proxy. No spider or active scan.
        # A public training API key protects against accidental browser use; this is not an exam boundary.
        base = 'http://webscan:8080'
        def zap(path, params=None):
            query = urlencode({'apikey': 'training-zap-local-only', **(params or {})})
            try:
                with urlopen(base + path + '?' + query, timeout=20) as response: value = json.load(response)
            except (OSError, ValueError) as exc: raise ValueError('ZAP no está listo. El docente debe ejecutar ./lab.sh webscan-on y volver a intentar.') from exc
            if 'code' in value: raise ValueError('ZAP rechazó la consulta: ' + str(value))
            return value
        version = zap('/JSON/core/view/version/')['version']
        # A unique query string scopes alerts to this run, even on a shared ZAP session.
        tag = 'ZAP-' + uuid.uuid4().hex
        observations = []
        for i, (route, token) in enumerate([('/vuln/documents/SALUD-001', 'training-agua-user'), ('/fixed/documents/SALUD-001', 'training-agua-user'), ('/fixed/documents/SALUD-001', 'training-salud-user'), ('/fixed/documents/SALUD-001', '')]):
            uri = 'http://gateway:8080/range' + route + '?run=' + tag
            raw = f'GET {uri} HTTP/1.1\r\nHost: gateway:8080\r\nX-Correlation-ID: {tag}-{i}\r\n'
            if token: raw += 'Authorization: Bearer ' + token + '\r\n'
            raw += '\r\n'
            response = zap('/JSON/core/action/sendRequest/', {'request': raw, 'followRedirects': 'false'})
            observations.append(response)
        for _ in range(40):
            if int(zap('/JSON/pscan/view/recordsToScan/').get('recordsToScan', '0')) == 0: break
            time.sleep(.25)
        else: raise ValueError('La cola pasiva no terminó; repite cuando ZAP esté listo.')
        alerts = zap('/JSON/core/view/alerts/', {'baseurl': 'http://gateway:8080/range', 'start': 0, 'count': 5000}).get('alerts', [])
        alerts = [a for a in alerts if tag in a.get('url', '')]
        report = {'tool': 'OWASP ZAP', 'version': version, 'mode': 'four fixed requests + passive analysis',
                  'episode': state['episode'], 'run': tag, 'requests': observations, 'alerts': alerts,
                  'limit': 'La ausencia de una alerta de autorización no demuestra ausencia de acceso entre clientes. Contrastar manualmente.'}
        result.update(zap_version=version, requests_sent=4, alerts_total=len(alerts),
                      report_sha256=hashlib.sha256(canonical(report)).hexdigest(), file=agent.write_student('zap-report.json', report))
    return result, json.dumps(result, ensure_ascii=False, indent=2)
