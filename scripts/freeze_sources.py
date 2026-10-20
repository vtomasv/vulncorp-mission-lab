"""Actualización explícita de fuentes públicas. No se ejecuta durante una clase."""
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]

def fetch(url):
    with urlopen(Request(url,headers={'User-Agent':'VulnCorp-Mission-Lab/0.1'}),timeout=40) as r:
        return json.load(r)

def main():
    locked=[]; meta=[]
    for package,version in [('Django','3.2'),('requests','2.31.0')]:
        url=f'https://pypi.org/pypi/{package}/{version}/json';data=fetch(url)
        wheels=[x for x in data['urls'] if x['filename'].endswith('py3-none-any.whl') or x['filename'].endswith('py2.py3-none-any.whl')]
        if len(wheels)!=1:raise RuntimeError('Revisar wheel de '+package)
        item=wheels[0];locked.append(f'{package}=={version} --hash=sha256:{item["digests"]["sha256"]}')
        meta.append({'package':package,'version':version,'source':url,'filename':item['filename'],'sha256':item['digests']['sha256']})
    (ROOT/'requirements-legacy.txt').write_text('# Paquetes vulnerables intencionales, NO importados por la aplicación activa.\n'+'\n'.join(locked)+'\n')
    epss_url='https://api.first.org/data/v1/epss?cve=CVE-2021-35042,CVE-2024-35195'
    epss=fetch(epss_url)
    kev_url='https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
    kev=fetch(kev_url)
    ids={'CVE-2021-35042','CVE-2024-35195'}
    snapshot={'retrieved_at':datetime.now(timezone.utc).isoformat(),'epss_source':epss_url,'epss':epss,
        'kev_source':kev_url,'kev_catalog_version':kev['catalogVersion'],
        'kev_matches':[x for x in kev['vulnerabilities'] if x['cveID'] in ids],
        'note':'Datos reales congelados. EPSS no es probabilidad local. Ausencia en KEV no prueba ausencia de explotación.'}
    (ROOT/'data/intelligence.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'data/packages-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('Fuentes congeladas:',len(meta),'paquetes;',len(epss['data']),'registros EPSS; KEV',kev['catalogVersion'])

if __name__=='__main__':main()
