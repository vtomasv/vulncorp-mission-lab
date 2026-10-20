"""Fixed same-origin HTTP/WebSocket tunnel to the private noVNC station. No arbitrary destination."""
import http.client
import select
import socket
from urllib.parse import unquote,urlsplit

def serve(handler):
    path=urlsplit(handler.path)
    relative=path.path[len('/desktop/'):]
    if any(part in ['.','..'] for part in unquote(relative).split('/')) or len(handler.path)>2500:
        handler.send_error(400);return
    upstream='/'+relative+('?' + path.query if path.query else '')
    if handler.headers.get('Upgrade','').lower()=='websocket':
        if relative!='websockify':handler.send_error(403);return
        origin=handler.headers.get('Origin')
        if origin and origin not in ['http://'+handler.headers.get('Host',''),'https://'+handler.headers.get('Host','')]:
            handler.send_error(403);return
        try:
            with socket.create_connection(('workstation',6080),timeout=5) as remote:
                header=f'GET {upstream} HTTP/1.1\r\nHost: workstation:6080\r\n'
                for key in ['Upgrade','Connection','Sec-WebSocket-Key','Sec-WebSocket-Version','Sec-WebSocket-Protocol','Origin']:
                    value=handler.headers.get(key)
                    if value:header+=key+': '+value+'\r\n'
                remote.sendall((header+'\r\n').encode('latin1'))
                # A raw tunnel preserves the WebSocket handshake and frames unchanged.
                remote.settimeout(None);handler.connection.settimeout(None)
                while True:
                    readable,_,_=select.select([remote,handler.connection],[],[],30)
                    for source in readable:
                        chunk=source.recv(65536)
                        if not chunk:return
                        (handler.connection if source is remote else remote).sendall(chunk)
        except OSError:
            return
        finally:handler.close_connection=True
    else:
        connection=http.client.HTTPConnection('workstation',6080,timeout=5)
        try:
            connection.request('GET',upstream);response=connection.getresponse()
            raw=response.read(8_000_001)
            if len(raw)>8_000_000:handler.send_error(413);return
            handler.send_response(response.status)
            handler.send_header('Content-Type',response.getheader('Content-Type','application/octet-stream'))
            handler.send_header('Content-Length',str(len(raw)));handler.send_header('Cache-Control','no-store')
            handler.send_header('X-Content-Type-Options','nosniff');handler.end_headers();handler.wfile.write(raw)
        except OSError:handler.send_error(503,'Puesto de trabajo no disponible')
        finally:connection.close()
