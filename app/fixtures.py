"""Datos del caso. Valores de negocio inventados, explícitamente docentes."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
CLIENTS = [
 {'id': 'salud', 'name': 'RedSalud Sur', 'sector': 'SALUD', 'icon': '✚', 'color': '#63e1ba',
  'mission': 'Que un resultado crítico llegue a tiempo a quien debe decidir.',
  'story': 'Son las 08:10. El laboratorio clínico debe entregar resultados urgentes. El portal de agenda factura más, pero los resultados sostienen decisiones clínicas. Todos los pacientes son ficticios.',
  'owner': 'Dra. Elisa Rojas · directora de operaciones clínicas', 'rto': '15 min', 'rpo': '5 min',
  'owner_cards': [
   {'id':'S-01','title':'Lo que el inventario no dice','text':'Los resultados de laboratorio llegan por la API de transferencia. El procedimiento manual atiende solo al 20% de la demanda. Pregunta qué ocurre si esa API se detiene.'},
   {'id':'S-02','title':'Una copia que no restaura no protege','text':'Las copias contienen el historial de resultados. Perder su disponibilidad puede impedir recuperarse dentro de la tolerancia del servicio.'}],
  'impacts': {'F-01':[2,1,1,2],'F-02':[4,3,4,3],'F-03':[5,5,4,3],'F-04':[3,2,3,2]},
  'normative': 'Condición OIV ficticia para el ejercicio; no corresponde a una institución real.'},
 {'id': 'agua', 'name': 'Aguas del Valle Sur', 'sector': 'AGUA', 'icon': '≈', 'color': '#74b9ff',
  'mission': 'Mantener la observación operacional y la capacidad de recuperar la telemetría.',
  'story': 'Son las 08:10. Un operador necesita reconstruir las últimas lecturas del historiador. Facturación puede esperar. Este caso representa dependencias de TI: no controla agua, válvulas ni una planta real.',
  'owner': 'Camila Soto · jefa de continuidad', 'rto': '30 min', 'rpo': '10 min',
  'owner_cards': [
   {'id':'A-01','title':'El servidor que parecía secundario','text':'El repositorio de copias permite reconstruir la telemetría histórica y decisiones del operador. Una cuenta con permisos demasiado amplios amenaza la recuperación.'},
   {'id':'A-02','title':'No confundir portal y operación','text':'La API pública entrega documentos administrativos. El portal no tiene una conexión con dispositivos físicos. El servicio esencial depende de otra cadena de datos.'}],
  'impacts': {'F-01':[1,1,1,1],'F-02':[2,1,2,2],'F-03':[5,5,3,4],'F-04':[4,3,2,3]},
  'normative': 'Calificación OIV simulada para funciones del dossier, no para toda aplicación de la empresa.'},
 {'id': 'digital', 'name': 'NubeAndes Servicios', 'sector': 'SERVICIOS DIGITALES', 'icon': '⌘', 'color': '#bfadff',
  'mission': 'Evitar que un error compartido se convierta en la exposición de todos los clientes.',
  'story': 'Son las 08:10. La misma API mueve documentos de varios clientes. Una exposición alcanza a múltiples organizaciones; el entorno legacy de demostración no recibe tráfico de clientes.',
  'owner': 'Diego Leiva · responsable de servicios gestionados', 'rto': '60 min', 'rpo': '15 min',
  'owner_cards': [
   {'id':'D-01','title':'La dependencia compartida','text':'La API de transferencia sirve a todos los clientes. La separación entre expedientes importa más que el conteo de vulnerabilidades de una biblioteca que no se usa.'},
   {'id':'D-02','title':'El costo del cambio','text':'Existe una ventana de 15 minutos y solo cuatro horas de ingeniería. Una restricción de acceso puede ser provisional: no equivale a corregir la causa raíz.'}],
  'impacts': {'F-01':[2,1,1,2],'F-02':[5,2,5,5],'F-03':[2,1,2,2],'F-04':[4,1,4,3]},
  'normative': 'Proveedor ficticio con alcance OIV definido solo para el caso académico.'}
]

FINDINGS = [
 {'id':'F-01','asset':'records','title':'La biblioteca crítica que nadie usa', 'kind':'CVE real / aplicabilidad por comprobar',
  'cve':'CVE-2021-35042','package':'Django','version':'3.2','severity':'CRITICAL','cvss':9.8,
  'vector':'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
  'description':'La imagen contiene Django 3.2 en /opt/legacy. La aplicación activa usa la biblioteca estándar de Python y no importa Django. El componente afectado está presente; no se demuestra una ruta explotable por su mera presencia.',
  'likelihood':1,'evidence':['EV-PACKAGES','EV-ARCHITECTURE'],'cwe':'CWE-89',
  'mitre':['T1190'],'iso':['A.8.8'],'law':'Ley 21.663 art. 8 a), d); aplicabilidad simulada.',
  'source':'https://www.djangoproject.com/weblog/2021/jul/01/security-releases/'},
 {'id':'F-02','asset':'gateway','title':'Un expediente ajeno, a un clic', 'kind':'Falla local reproducible',
  'cve':None,'package':'API de transferencia del curso','version':'0.1.0','severity':'HIGH','cvss':7.5,
  'vector':'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N',
  'description':'/api/export?tenant=sur devuelve expedientes sintéticos sin verificar la identidad del solicitante. La prueba se ejecuta desde la zona pública simulada. El vector es una valoración docente, no un CVE de un producto real.',
  'likelihood':4,'evidence':['EV-EXPORT'],'cwe':'CWE-862','mitre':['T1190','T1213.006'],'iso':['A.8.8','A.8.26'],
  'law':'Ley 21.663 art. 8 a), d), e); alcance del caso.', 'source':None},
 {'id':'F-03','asset':'backup','title':'La llave compartida de la recuperación', 'kind':'Configuración / sin CVE',
  'cve':None,'package':'Repositorio de copias','version':'0.1.0','severity':'CONTEXT','cvss':None,'vector':None,
  'description':'Una llave de entrenamiento compartida accede al catálogo de recuperación desde soporte. El catálogo declara privilegios de lectura y borrado; esta campaña no ejecuta borrado. Verificar copias, privilegios y consecuencias con el dueño.',
  'likelihood':3,'evidence':['EV-BACKUP'],'cwe':'CWE-798','mitre':['T1078'],'iso':['A.8.2','A.8.13','A.5.30'],
  'law':'Ley 21.663 art. 8 a), c); continuidad simulada.','source':None},
 {'id':'F-04','asset':'gateway','title':'El diagnóstico que salió de soporte', 'kind':'Falla local reproducible',
  'cve':None,'package':'Endpoint de diagnóstico','version':'0.1.0','severity':'MEDIUM','cvss':5.3,
  'vector':'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N',
  'description':'/api/diagnostics publica nombres de servicios y versiones desde una ruta que debía ser solo de soporte. El vector es docente. La exposición no prueba por sí sola movimiento lateral.',
  'likelihood':3,'evidence':['EV-DIAGNOSTICS'],'cwe':'CWE-200','mitre':[],'iso':['A.8.9','A.8.22'],
  'law':'Ley 21.663 art. 7 y 8 a); alcance simulado.','source':None},
 {'id':'F-05','asset':'records','title':'La dependencia presente con condiciones', 'kind':'CVE real / revisión de código',
  'cve':'CVE-2024-35195','package':'requests','version':'2.31.0','severity':'MEDIUM','cvss':5.6,
  'vector':'CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:H/A:N',
  'description':'requests 2.31.0 está en /opt/legacy. La vulnerabilidad depende del uso de una Session y de verify=False. El servicio no importa requests: presencia y afectación no prueban alcanzabilidad.',
  'likelihood':1,'evidence':['EV-PACKAGES','EV-ARCHITECTURE'],'cwe':'CWE-670','mitre':[],'iso':['A.8.8'],
  'law':'Registro de aplicabilidad; caso académico.','source':'https://github.com/psf/requests/security/advisories/GHSA-9wx4-h78v-vm56'},
 {'id':'VENDOR-06','asset':'records','title':'El mismo Django en otro reporte','kind':'Duplicado docente intencional',
  'cve':'CVE-2021-35042','package':'Django','version':'3.2','severity':'CRITICAL','cvss':9.8,'duplicate_of':'F-01',
  'vector':'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
  'description':'Reporte de proveedor sintético: mismo activo, componente, versión y CVE que F-01. No representa dos fallas independientes.',
  'likelihood':1,'evidence':['EV-VENDOR'],'cwe':'CWE-89','mitre':[],'iso':['A.8.8'],'law':'Caso docente.','source':None},
 {'id':'VENDOR-07','asset':'mission','title':'El escáner asegura algo que no está instalado','kind':'Falso positivo docente intencional',
  'cve':'CVE-2024-35195','package':'requests','version':'2.31.0','severity':'MEDIUM','cvss':5.6,'false_positive':True,
  'vector':None,'description':'El proveedor sintético atribuye requests al centro de misión. Esa imagen solo contiene el runtime Python y el código del curso, sin /opt/legacy. Contrastar contra el SBOM de la imagen correcta.',
  'likelihood':1,'evidence':['EV-VENDOR','EV-ARCHITECTURE'],'cwe':'CWE-670','mitre':[],'iso':['A.8.8'],'law':'Caso docente.','source':None}
]

ASSETS = [
 {'id':'gateway','name':'Gateway público','role':'Entrada de trámites y API','port':8080,'zones':['edge','app'],'owner':'Operación de aplicaciones','image':'vulncorp-core:0.1.0','data':'Tránsito de expedientes sintéticos'},
 {'id':'records','name':'Servicio de expedientes','role':'Datos y transacciones del negocio','port':8081,'zones':['app'],'owner':'Dueño del servicio','image':'vulncorp-records:0.1.0','data':'Expedientes sintéticos por cliente'},
 {'id':'backup','name':'Repositorio de recuperación','role':'Catálogo de copias y recuperación','port':8082,'zones':['support'],'owner':'Continuidad y soporte','image':'vulncorp-core:0.1.0','data':'Manifiestos sintéticos de copias'},
 {'id':'mission','name':'Centro de misión','role':'Gestión y evidencias del alumno','port':8000,'zones':['ui','edge','app','support','ai'],'owner':'Equipo de gestión','image':'vulncorp-core:0.1.0','data':'Decisiones docentes y evidencia'}
]

MISSIONS = [
 {'id':1,'title':'Lo que no ves también decide','subtitle':'Servicio → activo → exposición','brief':'El dueño pide proteger su servicio. Su inventario está incompleto. Tu primera misión es demostrar qué existe, desde dónde se alcanza y qué función sostiene.',
  'tasks':[
   {'id':'1-1','title':'Dibuja antes de escanear','instruction':'Lee el dossier, abre el portal y completa una transacción sintética. Explica qué servicio se perdería si records se detiene.','command':'./lab.sh probe public transaction','expected':'La transacción devuelve status=completed y un identificador. No prueba seguridad; prueba función.'},
   {'id':'1-2','title':'Mira desde dos lugares','instruction':'Ejecuta el descubrimiento desde público y soporte. Compara resultados DNS/TCP. Un puerto que no responde no es prueba de ausencia.','command':'./lab.sh discover public\n./lab.sh discover support','expected':'Público alcanza gateway; soporte alcanza backup. records no se alcanza directamente desde ninguna de esas dos zonas.'},
   {'id':'1-3','title':'Encuentra la puerta inesperada','instruction':'Prueba export y diagnostics desde público. Conserva respuesta y hora. No hay datos de personas reales.','command':'./lab.sh probe public export\n./lab.sh probe public diagnostics','expected':'La ruta export devuelve expedientes sin autenticar. diagnostics revela servicios. Explica qué demuestra cada respuesta.'},
   {'id':'1-4','title':'Pregunta al dueño','instruction':'Abre las tarjetas de contexto y registra una dependencia que no aparece en el inventario técnico.','expected':'La explicación relaciona al menos un activo con una función del cliente y una consecuencia.'}]},
 {'id':2,'title':'El ruido y la señal','subtitle':'SBOM → hallazgo → evidencia','brief':'Un proveedor entrega siete hallazgos. Hay CVEs reales, fallas del curso, un duplicado y un falso positivo. Tu trabajo es reconstruir la verdad sin confiar en la cantidad de alertas.',
  'tasks':[
   {'id':'2-1','title':'Abre la lista de ingredientes','instruction':'Genera SBOM de records y del centro de misión con Syft. Busca Django y requests y compara las imágenes.','command':'./lab.sh sbom','expected':'Los dos paquetes legacy aparecen en records, no en mission. Los reportes se guardan en artifacts/.'},
   {'id':'2-2','title':'Cruza software con vulnerabilidades','instruction':'Escanea el SBOM real con Grype. La primera vez descarga su base. El catálogo docente permanece congelado y rotulado.','command':'./lab.sh scan','expected':'Hay un reporte Grype real, versión de base y fecha. Su conteo puede cambiar y no tiene que coincidir con las siete tarjetas del caso.'},
   {'id':'2-3','title':'Investiga, no borres alertas','instruction':'Revisa código activo, ubicación del componente y advisory. Clasifica F-01, VENDOR-06 y VENDOR-07 con una razón y evidencia.','expected':'Distingues componente presente sin ruta demostrada, duplicado y atribución al activo equivocado.'},
   {'id':'2-4','title':'Saca la falla que el SBOM no ve','instruction':'Contrasta el escaneo con la prueba export de la clase 1. Explica por qué una falla de autorización sin CVE puede importar más.','expected':'La evidencia de función y acceso complementa al escáner de componentes.'}]},
 {'id':3,'title':'La prioridad cambia de dueño','subtitle':'Mismo hallazgo. Otra misión. Otra decisión.','brief':'Solo tienes cuatro horas de ingeniería y una ventana de quince minutos. Construye y defiende una cartera de tratamientos para tres clientes. Usa IA local para cuestionar tu análisis, conservando tu responsabilidad.',
  'tasks':[
   {'id':'3-1','title':'Decide con evidencia','instruction':'En Decisiones, evalúa F-01 a F-04. Elige L, cuatro impactos, entradas SSVC y justificación. El índice y el árbol se calculan automáticamente.','expected':'Cada decisión incluye dueño, evidencia y supuestos. Un índice de 80 no es 80% de probabilidad.'},
   {'id':'3-2','title':'Cambia el cliente, conserva los hechos','instruction':'Selecciona otro cliente y repite al menos F-02 y F-03. Abre Comparar. Explica qué premisa del negocio cambia la acción.','expected':'Salud y servicios digitales priorizan la API; agua da mayor peso a recuperación. Otras decisiones se aceptan con evidencia suficiente.'},
   {'id':'3-3','title':'Interroga a la IA local','instruction':'Activa el perfil CPU, carga Qwen3 y pide preguntas y opciones. Revisa fuentes y registra aceptar, corregir o rechazar.','command':'./lab.sh ai-prepare\n./lab.sh ai-on','expected':'El panel distingue inferencia real de ejemplo docente. El modelo no ejecuta comandos ni calcula riesgo.'},
   {'id':'3-4','title':'Cierra el ciclo','instruction':'Aplica una restricción temporal de exportación y repite export y transaction. Conserva ambas pruebas y registra el riesgo residual.','expected':'La exportación pública se bloquea, la transacción legítima funciona. Esto es mitigación temporal, no corrección de autorización.'}]}
]

CORPUS = [
 {'id':'EV-ARCHITECTURE','title':'Arquitectura verificada por el código','text':'gateway escucha 8080 en edge y app. records escucha 8081 solo en app. backup escucha 8082 solo en support. El centro de misión escucha 8000. El código activo usa la biblioteca estándar: /opt/legacy no se importa. Las redes target son internal:true. No hay Docker socket ni privilegios generales.','source':'compose.yaml; app/targets.py; Dockerfile','kind':'Código del laboratorio'},
 {'id':'EV-PACKAGES','title':'Componentes legacy reales','text':'La etapa records instala Django 3.2 y requests 2.31.0 en /opt/legacy con versiones y hashes fijados. Hay que verificarlo con Syft sobre la imagen exacta. Presencia de un paquete no demuestra uso de su función vulnerable.','source':'requirements-legacy.txt; Dockerfile','kind':'Verificar con SBOM real'},
 {'id':'EV-EXPORT','title':'Hipótesis de exportación pública','text':'La versión inicial de gateway deja pasar /api/export a records. records devuelve expedientes sintéticos sin autenticar. Se debe comprobar desde edge y guardar status, contenido y hora. Un bloqueo de gateway reduce exposición, pero no corrige la autorización en records.','source':'app/targets.py; prueba probe public export','kind':'Hipótesis hasta ejecutar la prueba'},
 {'id':'EV-BACKUP','title':'Catálogo de copias y permiso compartido','text':'backup solo es accesible desde support. La llave training-backup-key del caso accede al catálogo que declara permisos read y delete. Esta campaña no implementa borrado. Ni el catálogo ni una marca equivalen a una restauración probada.','source':'app/targets.py; prueba probe support backup','kind':'Hipótesis hasta ejecutar la prueba'},
 {'id':'EV-DIAGNOSTICS','title':'Diagnóstico publicado','text':'/api/diagnostics revela topología y versiones desde la entrada pública simulada. La lista de servicios no prueba acceso a sus redes. Después de restringir la ruta debe verificarse denegación y función legítima.','source':'app/targets.py','kind':'Hipótesis hasta ejecutar la prueba'},
 {'id':'EV-VENDOR','title':'Reporte de proveedor sintético','text':'VENDOR-06 repite F-01 en el mismo activo y componente. VENDOR-07 atribuye requests al centro de misión, donde no se instala. Son trampas docentes declaradas en la guía del instructor; no son resultados auténticos de Grype.','source':'data/findings.json','kind':'Datos sintéticos del ejercicio'},
 {'id':'EV-RISK','title':'Política docente de decisión','text':'El índice R=4×L×I usa L entre 1 y 5 e I máximo de operación, personas, datos y finanzas. Es ordinal; no porcentaje. SSVC Deployer DT_DP v1.0.0 usa explotación, exposición, automatización e impacto humano. Human Impact tiene su definición oficial y no equivale al I de esta fórmula. EPSS global no es probabilidad local; KEV no demuestra compromiso de este activo.','source':'app/risk.py; data/ssvc/deployer.json','kind':'Política docente y tabla CERT/CC'},
 {'id':'EV-CONTROLS','title':'Tratamientos y continuidad','text':'Restringir exportación cuesta 2 horas de ingeniería y cero minutos de interrupción en este caso. Rotar la llave cuesta 2 horas y 10 minutos. Restringir diagnóstico cuesta 1 hora y 5 minutos. Una mitigación no elimina una CVE ni prueba ausencia de compromiso. Se debe repetir una prueba de seguridad y una transacción de negocio.','source':'Política sintética de los tres clientes','kind':'Supuesto de negocio'}
]


def write_seed():
    for name, value in [('clients',CLIENTS),('findings',FINDINGS),('assets',ASSETS),('missions',MISSIONS),('corpus/evidence',CORPUS)]:
        (DATA / (name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


if __name__ == '__main__':
    write_seed()
