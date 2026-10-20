"""Sonda acotada a los tres targets. No admite URLs ni direcciones externas."""
import argparse
import json
import os
import socket
import sys
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError

TARGETS=[('gateway',8080),('records',8081),('backup',8082)]

def discover():
    observations=[]
    for name,port in TARGETS:
        try:
            address=socket.gethostbyname(name)
            try:
                with socket.create_connection((name,port),timeout=2):pass
                outcome='reachable'
            except OSError:outcome='not_reachable'
        except OSError:address=None;outcome='not_resolved_in_this_zone'
        observations.append({'target':name,'port':port,'address':address,'result':outcome})
    return {'zone':os.environ.get('LAB_ZONE','unknown'),'observed_at':datetime.now(timezone.utc).isoformat(),
            'targets':observations,'scope':'Tres targets del caso. No enumera el plano de gestión.',
            'limit':'Sin resolución o conexión no significa que el activo no exista.'}

def probe(action):
    routes={'transaction':'http://gateway:8080/api/transaction','export':'http://gateway:8080/api/export',
            'diagnostics':'http://gateway:8080/api/diagnostics','backup':'http://backup:8082/catalog'}
    headers={'X-Training-Key':'training-backup-key'} if action=='backup' else {}
    req=Request(routes[action],headers=headers)
    try:
        with urlopen(req,timeout=4) as r:status=r.status;body=json.load(r)
    except HTTPError as e:status=e.code;body=json.load(e)
    except OSError as e:status=0;body={'error':'Sin ruta o servicio no disponible','detail':str(e)}
    return {'zone':os.environ.get('LAB_ZONE','unknown'),'action':action,'url':routes[action],
            'observed_at':datetime.now(timezone.utc).isoformat(),'status':status,'body':body}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('discover')
    p=sub.add_parser('probe');p.add_argument('action',choices=['transaction','export','diagnostics','backup'])
    args=parser.parse_args()
    data=discover() if args.command=='discover' else probe(args.action)
    print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
