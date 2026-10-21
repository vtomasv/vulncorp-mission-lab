# Fuentes, hechos y analogías · consulta 21 octubre 2026

## Casos reales usados con límites explícitos

**Log4Shell.** La [guía conjunta publicada por CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a) distingue mitigaciones y búsqueda de actividad relacionada con vulnerabilidades de Log4j. Aquí se toma la pregunta metodológica: qué prueba un indicio y qué información hace falta para evaluar compromiso. El laboratorio no instala Log4j ni reproduce esas CVE; el callback y el marcador son un banco de medición explícito.

**MOVEit, 2023.** El [aviso CISA/FBI](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/35ecb08) documentó explotación de CVE-2023-34362 en MOVEit Transfer y actividad asociada a CL0P. Su mecanismo fue SQLi. Aquí se toma la necesidad de reconstruir conducta e investigar efectos posteriores al tratamiento. El rango usa una falla distinta de autorización de objetos; no reproduce el incidente ni atribuye al alumno su cadena de ataque.

**Synnovis, 2024.** [NHS England](https://www.england.nhs.uk/synnovis-cyber-incident/questions-and-answers/) describe la disrupción de capacidad de pruebas del proveedor de patología tras el ataque del 3 de junio de 2024. Sirve para conectar dependencias técnicas con función clínica. Salud Sur y sus efectos son ficticios; no se atribuye a Synnovis la falla técnica del rango ni una causa de acceso inicial que esa fuente no establezca.

## Métodos y herramientas

| Referencia primaria | Uso docente |
|---|---|
| [OWASP WSTG v4.2 · IDOR](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/) | Variar identidad/objeto y contrastar controles positivos y negativos. |
| [MITRE T1190](https://attack.mitre.org/techniques/T1190/) · v2.8 consultada | Conducta de abuso de aplicación accesible por gateway dentro de la simulación. |
| [MITRE T1078](https://attack.mitre.org/techniques/T1078/) · v3.0 consultada | Uso de cuenta que el guion declara comprometida; no acredita robo de la credencial. |
| [Navigator · formato 4.5](https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md) | Capa con dos técnicas y pruebas; no una base completa ATT&CK. |
| [ZAP · Docker oficial](https://www.zaproxy.org/docs/docker/about/) | Cuatro solicitudes acotadas y análisis pasivo, sin spider/escaneo activo. |
| [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) | Referencia a objetivos de control; no reproducción del estándar ni certificación. |

Las versiones de técnicas son metadatos de consulta; no se declara una versión de toda la matriz ATT&CK. Los resúmenes de controles ISO son paráfrasis docentes. Una asociación requiere interpretar alcance y eficacia con evidencias.

## Normativa chilena y fecha del caso

| Fuente | Distinción que se practica |
|---|---|
| [Ley 21.663](https://www.bcn.cl/leychile/navegar?i=1202434) · arts. 7, 8, 9 y 27 | Gestión, deberes del OIV ficticio, reporte y efecto significativo. |
| [DS 295/2024, publicado 1 marzo 2025](https://www.diariooficial.interior.gob.cl/publicaciones/2025/03/01/44088/01/2617387.pdf) | La afectación significativa puede incluir confidencialidad y acceso no autorizado, sin interrupción inmediata. Definiciones, información del reporte y gestión del incidente. |
| [Ley 21.459 · texto con versión 1 enero 2025](https://www.bcn.cl/leychile/Navegar?idNorma=1177743&idVersion=2025-01-01) | Necesidad de delimitar permiso del titular para pruebas del entorno. Este lab no enseña una autorización general para investigar terceros. |
| [Ley 19.628 · versión aplicable al caso antes de diciembre 2026](https://www.bcn.cl/leychile/Navegar?idNorma=141599&idVersion=2023-05-09) | Datos de salud y tratamiento de datos; aquí solo hay datos sintéticos. |
| [BCN · vigencia de Ley 21.719](https://www.bcn.cl/balance-legislativo/detalle/ficha_LEY_21719_2024-12-13) | Reforma entra el 1 diciembre 2026; el caso se fija al 21 octubre de 2026. |

El motor calcula la regla docente del art. 9 sobre horas fijas del dossier. El final toma como base el envío de la alerta temprana; la actualización especial requiere OIV y afectación del servicio esencial. El plan de acción OIV se informa al adoptarlo y su adopción tiene máximo de siete días corridos desde conocimiento. Un incidente aún en curso exige informe de situación y posterior final desde su gestión. Los borradores no sustituyen formularios oficiales ni todos sus campos. No hay envío a autoridades ni aceptación legal de decisiones por la plataforma.

Antes de impartir el curso en otra fecha, revisar vigencias y mantener separada la fecha del escenario. La política de excepción de treinta días es inventada para discutir gobierno: no proviene de una norma.
