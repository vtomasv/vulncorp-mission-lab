"""Small isolated measurement range. This is NOT a Log4j/CVE exploit replica.

The authorization flaw is real. The callback/child-process rig teaches proof limits;
it accepts neither a command nor a URL from the learner. No personal data is used.
"""
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from .secure import secret

KEY = secret('control')
LOCK = threading.RLock()
BOOT = uuid.uuid4().hex
STATE = {'campaign': None, 'episode': None, 'authz_fixed': False, 'revoked': False}
SESSIONS = {}
EVENTS = []
SEQUENCE = 0
STATE_FILE = Path(os.environ['LAB_RANGE_STATE']) if os.environ.get('LAB_RANGE_STATE') else None
if STATE_FILE and STATE_FILE.exists():
    saved = json.loads(STATE_FILE.read_text())
    STATE.update(saved['state'])
    EVENTS[:] = saved['events']
    SEQUENCE = saved['sequence']
    SESSIONS.update(saved.get('sessions', {}))


def persist():
    if STATE_FILE:
        temporary = STATE_FILE.with_suffix('.tmp')
        temporary.write_text(json.dumps({'state':STATE,'events':EVENTS,'sequence':SEQUENCE,'sessions':SESSIONS},ensure_ascii=False))
        temporary.chmod(0o600)
        temporary.replace(STATE_FILE)
TOKENS = {'training-agua-user': 'agua', 'training-salud-user': 'salud', 'training-stolen-salud': 'salud'}
DOCS = {'SALUD-001': {'tenant': 'salud', 'value': 'RESULTADO FICTICIO DE ENTRENAMIENTO'},
        'AGUA-001': {'tenant': 'agua', 'value': 'LECTURA FICTICIA DE ENTRENAMIENTO'}}


def event(kind, **data):
    global SEQUENCE
    with LOCK:
        SEQUENCE += 1
        row = {'id': 'RNG-' + uuid.uuid4().hex, 'sequence': SEQUENCE,
               'occurred_at': time.time(), 'boot_id': BOOT, **STATE, 'kind': kind, **data}
        EVENTS.append(row)
        del EVENTS[:-3000]
        persist()
        return row


class Range(BaseHTTPRequestHandler):
    def log_message(self, *args): pass

    def reply(self, body, status=200):
        raw = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def trusted(self):
        return self.headers.get('X-Lab-Control') == KEY

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/health': return self.reply({'ok': True})
        if path in ['/_audit', '/_status']:
            if not self.trusted(): return self.reply({'error': 'Canal privado'}, 403)
            with LOCK: return self.reply({'state': dict(STATE), 'boot_id': BOOT, 'events': list(EVENTS) if path == '/_audit' else []})
        if os.environ.get('LAB_RANGE_ROLE') == 'collector': return self.reply({'error': 'Sin ruta pública'}, 404)
        if not STATE['episode']: return self.reply({'error': 'Ejecuta lab abrir desde aplicaciones.'}, 409)
        peer = self.client_address[0]
        origin = self.headers.get('X-Training-Origin', peer) if self.headers.get('X-Gateway-Key') == KEY else peer
        correlation = self.headers.get('X-Correlation-ID', '')[:80] or uuid.uuid4().hex
        parts = path.strip('/').split('/')
        if len(parts) == 3 and parts[0] in ['vuln', 'fixed', 'live'] and parts[1] == 'documents':
            token = self.headers.get('Authorization', '').removeprefix('Bearer ')
            tenant = TOKENS.get(token)
            doc = DOCS.get(parts[2])
            protected = parts[0] == 'fixed' or (parts[0] == 'live' and STATE['authz_fixed'])
            status = 401 if not tenant or (token == 'training-stolen-salud' and STATE['revoked']) else 404 if not doc else 403 if protected and tenant != doc['tenant'] else 200
            row = event('document', peer=peer, origin=origin, correlation=correlation, route=path,
                        status=status, identity=token or 'anonymous', tenant=tenant,
                        document=parts[2], document_tenant=doc['tenant'] if doc else None)
            return self.reply({'synthetic': True, 'event_id': row['id'], 'correlation': correlation,
                               'status': status, 'document': doc if status == 200 else None}, status)
        if path in ['/rig/callback', '/rig/marker']:
            phase = event('request', peer=peer, origin=origin, correlation=correlation, route=path, status=200)
            execution = None
            if path.endswith('/marker'):
                # Fixed executable + fixed program, no shell and no learner arguments.
                process = subprocess.run([sys.executable, '-I', '-c', 'print("TRAINING-MARKER-ONLY")'], capture_output=True, text=True, timeout=3, check=True)
                execution = event('marker', correlation=correlation, parent=phase['id'],
                                  output=process.stdout.strip(), sha256=hashlib.sha256(process.stdout.encode()).hexdigest(), exit_code=process.returncode)
            payload = {'campaign': STATE['campaign'], 'episode': STATE['episode'], 'correlation': correlation,
                       'parent': phase['id'], 'marker': execution['id'] if execution else None}
            request = Request('http://collector:8084/collect', data=json.dumps(payload).encode(),
                              headers={'Content-Type': 'application/json', 'X-Lab-Control': KEY})
            try:
                with urlopen(request, timeout=3) as response: receipt = json.load(response)
            except (OSError, ValueError): return self.reply({'error': 'Colector interno no disponible'}, 503)
            row = event('callback', correlation=correlation, parent=phase['id'], receipt=receipt['event_id'], status=200)
            return self.reply({'synthetic': True, 'rig': 'measurement-not-CVE', 'request': phase['id'],
                               'execution': execution, 'callback': row, 'collector': receipt})
        return self.reply({'error': 'Fuera del alcance'}, 404)

    def do_POST(self):
        if not self.trusted(): return self.reply({'error': 'Canal privado'}, 403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4096: raise ValueError()
            data = json.loads(self.rfile.read(length))
            with LOCK:
                if self.path == '/collect' and os.environ.get('LAB_RANGE_ROLE') == 'collector':
                    row = event('collector', campaign=data['campaign'], episode=data['episode'],
                                correlation=data['correlation'], parent=data['parent'], marker=data.get('marker'))
                    return self.reply({'event_id': row['id'], 'correlation': row['correlation']})
                if self.path != '/_control': return self.reply({'error': 'Fuera del alcance'}, 404)
                action = data.get('action')
                if action == 'open':
                    campaign = data.get('campaign')
                    if not isinstance(campaign, str) or not 5 <= len(campaign) <= 100: raise ValueError()
                    if campaign != STATE['campaign']:
                        if STATE['campaign']: SESSIONS[STATE['campaign']] = dict(STATE)
                        STATE.update(SESSIONS.get(campaign) or dict(campaign=campaign, episode='EP-' + uuid.uuid4().hex, authz_fixed=False, revoked=False))
                        event('opened')
                elif not STATE['episode']: return self.reply({'error': 'Abre primero el expediente'}, 409)
                elif action == 'fix': STATE['authz_fixed'] = True; event('control', action='fix')
                elif action == 'revoke': STATE['revoked'] = True; event('control', action='revoke')
                else: raise ValueError()
                return self.reply({'state': dict(STATE), 'boot_id': BOOT})
        except (ValueError, KeyError, TypeError): return self.reply({'error': 'Solicitud fuera del contrato'}, 400)


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8084 if os.environ.get('LAB_RANGE_ROLE') == 'collector' else 8083), Range).serve_forever()
