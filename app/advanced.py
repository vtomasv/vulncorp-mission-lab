"""Evidence-backed continuation: scope, authorization, ATT&CK and a fictional OIV.

XP verifies reproducible observations and structural relationships, never argument
quality, legal compliance, attribution or authority to accept organizational risk.
"""
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

CONFIG = json.loads((Path(__file__).resolve().parents[1] / 'data/advanced.json').read_text())
IDS = set(CONFIG['exercises'])


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def deadline(known, early_sent, oiv, essential_affected, ongoing=False, managed=None):
    """Ley 21.663 art. 9: final counted from EARLY ALERT, never the update.

    UTC inputs with explicit offsets; no execution-time countdown. A planned
    outage is not automatically a significant incident (Reglamento art. 4).
    """
    def instant(value):
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if dt.tzinfo is None: raise ValueError('Indica zona horaria, por ejemplo Z para UTC.')
        return dt.astimezone(timezone.utc)
    def fmt(value): return value.isoformat().replace('+00:00', 'Z')
    knowledge, early = instant(known), instant(early_sent)
    if early < knowledge or early > knowledge + timedelta(hours=3):
        raise ValueError('La alerta debe enviarse desde el conocimiento y dentro de las primeras 3 horas del caso.')
    result = {'early_due': fmt(knowledge + timedelta(hours=3)),
              'update_due': fmt(knowledge + timedelta(hours=24 if oiv and essential_affected else 72)),
              'final_due': fmt(early + timedelta(days=15)),
              'action_due': fmt(knowledge + timedelta(days=7)) if oiv else None,
              'final_kind': 'status' if ongoing else 'final'}
    if managed:
        resolved = instant(managed)
        if resolved < knowledge: raise ValueError('La gestión no puede preceder al conocimiento.')
        result['managed_final_due'] = fmt(resolved + timedelta(days=15))
    return result


def current_records(store, kind, run):
    return [r for r in store.records(kind) if r.get('game_run') == run['id']]


def range_state(store):
    response = store.request_target('http://validation:8083/_status', headers={'X-Lab-Control': store.CONTROL_KEY})
    return response.get('body', {}).get('state', {}) if response.get('status') == 200 else {}


def collect(store, addresses):
    """Read actual target/collector logs over the private channel, not browser files."""
    known = {r['id'] for r in store.records('lab_event')}
    for host, port in [('validation', 8083), ('collector', 8084)]:
        response = store.request_target(f'http://{host}:{port}/_audit', headers={'X-Lab-Control': store.CONTROL_KEY})
        for event in response.get('body', {}).get('events', []):
            if event['id'] not in known:
                store.save('lab_event', {**event, 'actor': addresses.get(event.get('origin')),
                                        'provenance': host + '-audit',
                                        'content_sha256': hashlib.sha256(canonical(event)).hexdigest()})
                known.add(event['id'])


def evidence(store, run, state):
    return [r for r in store.records('lab_event') if r.get('campaign') == run['id']
            and r.get('episode') == state.get('episode') and r.get('occurred_at', 0) >= run['started']]


def record(store, data):
    from . import continuation
    if data.get('challenge_id') in continuation.IDS:return continuation.record(store,data)
    from . import game
    run = game.campaign(store)
    item = game.current(store, run)
    if not item or data.get('challenge_id') != item['id'] or item['id'] not in IDS:
        raise ValueError('Registra el análisis del objetivo activo de esta campaña.')
    spec = CONFIG['exercises'][item['id']]
    answers = data.get('answers')
    if not isinstance(answers, dict): raise ValueError('Completa las preguntas del objetivo.')
    clean = {}
    for page in spec['pages']:
        for field in page['fields']:
            value = store.nonempty(answers.get(field['key']), field.get('min', 1), field.get('max', 1800))
            if 'options' in field and value not in [o[0] for o in field['options']]:
                raise ValueError('Selecciona una de las opciones de ' + field['label'])
            if 'expected' in field and value != field['expected']:
                raise ValueError(field['feedback'])
            clean[field['key']] = value
    state = range_state(store)
    if state.get('campaign') != run['id']: raise ValueError('Ejecuta lab abrir en aplicaciones para vincular este rango a tu campaña.')
    rows = evidence(store, run, state)
    refs = data.get('evidence_ids', [])
    known = {r['id'] for r in rows}
    if not isinstance(refs, list) or len(refs) > 30 or any(r not in known for r in refs):
        raise ValueError('Selecciona fuentes auténticas del episodio actual, no IDs inventados o históricos.')
    if item['id'] != 'alcance' and not refs: raise ValueError('Vincula al menos un evento real del rango.')
    if item['id'] == 'cronologia':
        sequence = [x['id'] for x in rows if x['kind'] == 'document' and x.get('correlation', '').startswith('SIM-') and x.get('actor') == 'appdesk'][-3:]
        provided = [v.strip() for v in clean['order'].replace(',', '\n').splitlines() if v.strip()]
        if len(sequence) != 3 or provided != sequence:
            raise ValueError('Ordena los tres eventos SIM más recientes por su secuencia del servidor. No uses el orden visual del listado.')
    if item['id'] == 'mapeo':
        linked = {r['id']: r for r in rows if r['id'] in refs and r.get('actor') == 'appdesk'}
        a, b = linked.get(clean['t1190'], {}), linked.get(clean['t1078'], {})
        if not (a.get('identity') == 'training-agua-user' and a.get('document_tenant') == 'salud' and a.get('status') == 200
                and a.get('correlation', '').startswith('SIM-') and b.get('identity') == 'training-stolen-salud' and b.get('status') == 200
                and b.get('correlation', '').startswith('SIM-')):
            raise ValueError('Vincula a cada técnica el evento SIM que realmente demuestra esa conducta simulada.')
    if item['id'] == 'reportes':
        incident=CONFIG['incident']
        a=deadline(incident['known_at'],incident['early_sent_at'],True,True)
        b=deadline(incident['known_at'],incident['early_sent_at'],True,False)
        d=deadline(incident['known_at'],incident['early_sent_at'],True,True,True,incident['managed_at'])
        expected_answers={'early':a['early_due'],'updateA':a['update_due'],'updateB':b['update_due'],
                          'action':a['action_due'],'final':a['final_due'],'managed':d['managed_final_due']}
        for key, expected in expected_answers.items():
            try: same = datetime.fromisoformat(clean[key].replace('Z', '+00:00')) == datetime.fromisoformat(expected.replace('Z', '+00:00'))
            except ValueError: same = False
            if not same: raise ValueError('Revisa ' + key + ': usa el conocimiento para alerta/actualización/plan y el envío de alerta temprana para el informe final. Indica zona horaria.')
    if item['id'] == 'matriz':
        available=store.known_evidence() | {r['id'] for r in store.records('station') if r.get('occurred_at',0)>=run['started']}
        for fid in ['F-01','F-02','F-03','F-04','F-05']:
            if not any(ref in clean[fid+'_reason'] for ref in available):
                raise ValueError('Cita en '+fid+' al menos un ID existente del corpus o de tus pruebas anteriores. Consulta el expediente original.')
    if item['id'] == 'excepcion':
        expiry = datetime.fromisoformat(clean['expiry'].replace('Z', '+00:00'))
        start = datetime.fromisoformat(CONFIG['incident']['known_at'].replace('Z', '+00:00'))
        if expiry.tzinfo is None or not start < expiry <= start + timedelta(days=30):
            raise ValueError('La política ficticia limita esta excepción a 30 días desde el conocimiento. Indica vencimiento con zona horaria.')
        trial = [r for r in rows if r['id'] in refs and r['kind'] == 'document' and r.get('revoked') and r.get('authz_fixed')]
        if not any(r['status'] == 200 for r in trial) or not any(r['status'] in [401, 403] for r in trial):
            raise ValueError('La excepción necesita pruebas actuales de bloqueo y función legítima; una asociación ISO no las reemplaza.')
    if item['id'] == 'auditoria':
        audits = current_records(store, 'ai', run)
        audit = next((a for a in reversed(audits) if a.get('purpose') == 'oiv-dossier' and a.get('episode') == state['episode']), None)
        if not audit: raise ValueError('Ejecuta primero lab ia-expediente en aplicaciones.')
        if audit['validation_errors'] and clean['verdict'] == 'accept':
            raise ValueError('Hay errores en la salida: corrige o rechaza la propuesta.')
        clean['audit_id'] = audit['id']
        # The prose must identify a claim and contrast it, not merely approve a model.
        if not any(source in clean['reason'] for source in audit['source_ids']):
            raise ValueError('Cita en tu revisión al menos un ID de las fuentes que recibió el modelo y explica si respalda la afirmación.')
    return store.save('lab_record', {'challenge_id': item['id'], 'answers': clean, 'evidence_ids': list(dict.fromkeys(refs)),
                                    'episode': state['episode'], 'game_run': run['id'],
                                    'checked': 'Relaciones y estructura comprobadas; fundamento para revisión humana.'})


def conditions(store, challenge, run):
    id = challenge['id']
    if id not in IDS:
        from . import continuation
        return continuation.conditions(store,challenge,run)
    state = range_state(store)
    rows = evidence(store, run, state)
    stations = [r for r in store.records('station') if r.get('occurred_at', 0) >= run['started']
                and r.get('station') == 'appdesk' and r.get('result', {}).get('episode') == state.get('episode')
                and r.get('result', {}).get('campaign') == run['id']]
    notes = [r for r in current_records(store, 'lab_record', run) if r['challenge_id'] == id and r['episode'] == state.get('episode')]
    checks = []
    def check(label, ok, proofs=()): checks.append({'label': label, 'ok': bool(ok), 'proof_ids': [p['id'] for p in proofs]})
    def command(action):
        found = [r for r in stations if r['action'] == action]
        check('Prueba desde aplicaciones: lab ' + action, found, found)
        return found
    docs = [r for r in rows if r['kind'] == 'document' and r.get('actor') == 'appdesk']
    check('Rango disponible y vinculado a esta campaña', state.get('campaign') == run['id'])
    if id == 'alcance': command('abrir')
    elif id in ['callback', 'marcador']:
        command('callback' if id == 'callback' else 'marcador')
        requests = [r for r in rows if r['kind'] == 'request' and r.get('actor') == 'appdesk'
                    and r.get('route') == ('/rig/callback' if id == 'callback' else '/rig/marker')]
        linked = [r for r in rows if r['kind'] == 'collector' and any(r.get('parent') == q['id'] and r['correlation'] == q['correlation'] for q in requests)]
        check('Solicitud y callback correlacionados en servicios distintos', linked, linked)
        if id == 'marcador':
            markers = [r for r in rows if r['kind'] == 'marker' and r.get('exit_code') == 0 and any(r.get('parent') == q['id'] for q in requests)]
            check('Subproceso fijo observado; no una explotación de CVE', markers, markers)
    elif id == 'tenants':
        command('transferencia')
        for route, identity, status in [('/vuln/documents/SALUD-001', 'training-agua-user', 200),
                                       ('/fixed/documents/SALUD-001', 'training-agua-user', 403),
                                       ('/fixed/documents/SALUD-001', 'training-salud-user', 200),
                                       ('/fixed/documents/SALUD-001', 'anonymous', 401)]:
            found = [r for r in docs if r['route'] == route and r['identity'] == identity and r['status'] == status]
            check(f'{route}: {identity} → {status}', found, found)
    elif id == 'contraste-zap':
        found = command('zap')
        check('ZAP real con versión, tráfico propio y reporte', any(r['result'].get('zap_version') and r['result'].get('requests_sent') == 4 and r['result'].get('report_sha256') for r in found), found)
    elif id == 'dictamen':
        check('Conclusión vincula varias pruebas del episodio', notes and len(set(notes[-1]['evidence_ids'])) >= 2, notes)
    elif id == 'simulacion':
        command('simular')
        found = [r for r in docs if r.get('correlation', '').startswith('SIM-')]
        check('Acceso entre clientes y uso de identidad comprometida simulados', any(r['identity'] == 'training-agua-user' and r['status'] == 200 for r in found) and any(r['identity'] == 'training-stolen-salud' and r['status'] == 200 for r in found), found)
    elif id == 'cronologia': command('cronologia')
    elif id == 'mapeo':
        check('Dos técnicas sustentadas y cifrado descartado por falta de prueba', notes, notes)
    elif id in ['autorizacion', 'revocacion']:
        command('corregir' if id == 'autorizacion' else 'revocar')
        trials = [r for r in docs if r.get('correlation', '').startswith('TEST-')]
        fixed, revoked = True, id == 'revocacion'
        after = [r for r in trials if r.get('authz_fixed') == fixed and r.get('revoked') == revoked]
        before = [r for r in trials if r.get('authz_fixed') == (False if id == 'autorizacion' else True) and not r.get('revoked')]
        change = next((r for r in reversed(rows) if r['kind'] == 'control' and r.get('action') == ('fix' if id == 'autorizacion' else 'revoke')), None)
        before = [r for r in before if change and r['occurred_at'] < change['occurred_at']]
        after = [r for r in after if change and r['occurred_at'] > change['occurred_at']]
        expected_before={'training-agua-user':200 if id=='autorizacion' else 403,'training-salud-user':200,'training-stolen-salud':200}
        check('Tres identidades ensayadas antes del cambio', all(any(r['identity']==token and r['status']==status for r in before) for token,status in expected_before.items()), before)
        for identity, status in [('training-agua-user', 403), ('training-salud-user', 200), ('training-stolen-salud', 401 if revoked else 200)]:
            found = [r for r in after if r['identity'] == identity and r['status'] == status]
            check(f'Después: {identity} → {status}', found, found)
        check('El estado del control continúa vigente', state.get('authz_fixed') and bool(state.get('revoked')) == revoked)
    elif id == 'capa':
        found = command('capa')
        layer_hash = hashlib.sha256(canonical(layer(store, run))).hexdigest()
        check('Capa Navigator enlaza el análisis humano y el episodio actual', any(r['result'].get('layer_sha256') == layer_hash for r in found), found)
    elif id == 'incidente': command('incidente')
    elif id == 'auditoria':
        found = command('ia-expediente')
        audit_ids = {r['result'].get('audit_id') for r in found}
        audits = [r for r in current_records(store, 'ai', run) if r['id'] in audit_ids and r.get('purpose') == 'oiv-dossier' and r.get('mode') == 'live-local']
        check('Consulta real local sobre pruebas actuales y fuente legal', audits, audits)
    check('Análisis, fundamento y fuentes registrados', notes, notes)
    return checks


def layer(store, run):
    state = range_state(store)
    notes = [r for r in current_records(store, 'lab_record', run) if r['challenge_id'] == 'mapeo' and r['episode'] == state.get('episode')]
    if not notes: return {'error': 'Primero registra el mapeo sustentado.'}
    note = notes[-1]
    return {'name': 'VulnCorp · conductas observadas en simulación', 'domain': 'enterprise-attack',
            'versions': {'navigator': '5.2.0', 'layer': '4.5'},
            'description': 'Subconjunto observado, no cobertura completa ni atribución. ' + state['episode'],
            'techniques': [{'techniqueID': tid, 'color': '#8d79ad', 'enabled': True,
                            'comment': f"Simulación declarada; evidencia {note['answers'][key]}; análisis {note['id']}. {note['answers']['reason']}"}
                           for tid, key in [('T1190', 't1190'), ('T1078', 't1078')]],
            'metadata': [{'name': 'campaign', 'value': run['id']}, {'name': 'episode', 'value': state['episode']},
                         {'name': 'technique versions', 'value': 'T1190 v2.8; T1078 v3.0; consultadas 2026-10-21'}]}


def ai_dossier(store):
    from . import game, ai
    run = game.campaign(store)
    if (game.current(store, run) or {}).get('id') != 'auditoria': raise ValueError('La consulta del expediente se abre al llegar a su objetivo.')
    state = range_state(store)
    events = evidence(store, run, state)
    trials = [r for r in events if r['kind'] == 'document' and r.get('authz_fixed') and r.get('revoked')][-3:]
    if len(trials) < 3: raise ValueError('Faltan las pruebas posteriores a ambos controles.')
    docs = [{'id': r['id'], 'title': 'Observación real del rango', 'text': json.dumps({k: r.get(k) for k in ['identity','route','status','authz_fixed','revoked','correlation']}, ensure_ascii=False)} for r in trials]
    docs.append({'id': 'LAW-ART9', 'title': 'Ley 21.663 art. 9 · paráfrasis docente',
                 'text': CONFIG['legal_summary'], 'url': CONFIG['sources'][0]['url']})
    result = ai.propose('salud', 'Redacta una síntesis para el dueño: distingue el acceso observado, el efecto de autorización y de revocación, y los límites. Cita cada afirmación y no declares cumplimiento legal.', ['F-02'], documents=docs)
    return store.save('ai', {**result, 'client_id': 'salud', 'finding_ids': ['F-02'], 'purpose': 'oiv-dossier', 'episode': state['episode']})
