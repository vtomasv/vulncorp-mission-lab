"""Fixed TCP bridge: local student SSH reaches ONLY the internal analysis station.

SSH authentication/encryption terminate at workstation's sshd, never in this relay.
The fixed destination preserves the edge-only network of the analysis workstation.
"""
import select
import socket
import socketserver
import threading

SLOTS=threading.BoundedSemaphore(16)

class Connection(socketserver.BaseRequestHandler):
    def handle(self):
        if not SLOTS.acquire(blocking=False):return
        try:
            with socket.create_connection(('workstation',2222),timeout=5) as upstream:
                upstream.settimeout(None)
                while True:
                    readable,_,_=select.select([self.request,upstream],[],[],30)
                    for source in readable:
                        data=source.recv(65536)
                        if not data:return
                        (upstream if source is self.request else self.request).sendall(data)
        except OSError:pass
        finally:SLOTS.release()

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
    daemon_threads=True

def start():
    server=Server(('0.0.0.0',2222),Connection)
    threading.Thread(target=server.serve_forever,daemon=True,name='student-ssh').start()
    return server
