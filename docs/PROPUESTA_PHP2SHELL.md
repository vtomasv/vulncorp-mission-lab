# Propuesta de misión: PHP2Shell, de la alerta al servicio verificado

Estado: **nivel 1 implementado y verificado**. La propuesta original se conserva abajo como antecedente de diseño; las instrucciones operativas y diferencias finales están en [CONTINUACION_7_10.md](CONTINUACION_7_10.md) y [VALIDACION_7_10.md](VALIDACION_7_10.md). No se implementó el nivel 2 de reproducción RCE. Consulta de fuentes: **21 de octubre de 2026**.

## Qué caso se estudiará

PHP2Shell es el nombre usado para las vulnerabilidades **CVE-2026-109618** y **CVE-2026-109619**, divulgadas por PHP en octubre de 2026. Se estudiarán a partir de los avisos del proyecto y del proveedor de la distribución elegida. No se sustituirá ese caso por una webshell PHP genérica ni se presentará un subproceso sintético como explotación de esas CVE.

- [Aviso PHP, GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w): CVE-2026-109618, corrupción relacionada con el manejo de falta de memoria. El comportamiento y la posibilidad de explotación varían según SAPI y condiciones.
- [Aviso PHP, GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp): CVE-2026-109619, estado global obsoleto asociado al ciclo de solicitudes. La relación entre solicitudes y trabajador es relevante para analizar las condiciones.
- [Anuncio oficial PHP](https://www.php.net/archive/2026.php): identifica las ramas corregidas. El módulo congelará una pareja de compilaciones y sus avisos al prepararlo.
- [CERT-EU, 2026-018](https://cert.europa.eu/publications/security-advisories/2026-018): recomienda actualizar. Las mitigaciones parciales no sustituyen la corrección completa.
- [Declaración conjunta ENISA](https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities): permite discutir el inventario de servicios y la coordinación con proveedores ante una divulgación crítica.

Los avisos se están actualizando. Antes de construir se conservará una copia fechada, su hash, la revisión consultada y las diferencias con la consulta anterior. La práctica no asumirá que una prueba sirve para todos los SAPI o arquitecturas. En particular, una demostración publicada para `mod_php` no se trasladará automáticamente a PHP-FPM.

## La experiencia que verá el estudiante

El cliente ficticio NubeAndes mantiene un portal PHP de intercambio de documentos sintéticos. El dueño pide conservar una transacción legítima y reducir la exposición. Un proveedor responde: «Ya actualizamos PHP». La estación muestra una versión CLI nueva, pero el expediente todavía debe acreditar qué proceso web atiende solicitudes.

La sorpresa se construye con una discrepancia verificable: **tener una imagen corregida disponible o un CLI nuevo no garantiza que el servicio activo la esté usando**. Una decisión de cierre necesita identificar el despliegue real, los trabajadores activos, el alcance de la prueba y la función del cliente. No se fabricará una salida falsa de `php -v`: si se presenta una discrepancia, habrá dos instalaciones o despliegues reales, identificados como tales, dentro del escenario.

Otra tarjeta del caso ofrece una mitigación de configuración tomada de un aviso. El alumno debe explicar a qué CVE y condición se refiere, qué queda pendiente y qué riesgo de disponibilidad puede introducir. No se propondrá eliminar límites de memoria del contenedor para forzar una reproducción. El objetivo final será una decisión de tratamiento defendible, acompañada de pruebas posteriores.

## Encaje en lo que falta del curso

| Tramo previsto | Papel del caso PHP2Shell | Trabajo cognitivo y producto |
|---|---|---|
| Clase 7: evaluar y proteger al asistente | Analizar un dossier con avisos primarios y una nota sintética que mezcla condiciones de las dos CVE | Comparar respuesta manual/IA, detectar una referencia correcta usada para una conclusión incorrecta y conservar la revisión |
| Clase 8: remediar sin perder el servicio | Seleccionar y aplicar el cambio de una pareja de imágenes reproducibles | Demostrar estado anterior y posterior, proceso web activo, prueba pertinente y operación legítima. Añadir reversión y restauración solo si están implementadas y medidas |
| Clase 9: operación continua y crisis | Recibir un cambio de exposición, proveedor o nueva revisión del aviso | Reabrir una decisión, depurar hallazgos, actualizar excepción y explicar métricas por servicio |
| Clase 10: integración final | Transferir el método a un caso nuevo de dificultad practicada | Mantener un único examen final. La práctica pública no revelará el expediente ni las respuestas de la evaluación |

El contenido no depende de cuánto tarde un comando. Cada acción se acompaña de predicción, lectura de evidencia, contraprueba y defensa. Los desafíos intermedios son formativos. Los PX conservan su función de avance del juego.

## Arquitectura Docker propuesta

Se conservará el acceso noVNC/SSH al mismo puesto de análisis y el salto interno a aplicaciones. La plataforma web seguirá mostrando instrucciones, formularios y avance de la campaña.

| Componente | Función | Frontera propuesta |
|---|---|---|
| Puesto de aplicaciones existente | Ejecutar clientes y revisar archivos de evidencia | Solo redes previstas del rango, sin puertos nuevos al anfitrión |
| Gateway del caso PHP | Representar el borde del portal ficticio y registrar peticiones | Solo rutas y destinos internos autorizados, sin proxy libre |
| Target PHP | Atender una operación legítima y las pruebas seleccionadas | Sin Internet, sin privilegios, sin socket Docker ni montajes del equipo |
| Colector/verificador | Conservar petición, resultado, proceso y estado del despliegue | Instrumentación separada del contenido que el alumno puede cambiar |
| Almacén de evidencia | Vincular observaciones a campaña y episodio | Recibos y hashes, sin permitir que un archivo editado por el alumno acredite ejecución |
| Ollama existente | Redactar y contrastar un dossier limitado | Sin permisos de ejecutar herramientas, cambiar controles o aceptar riesgo |

El target usará usuario sin privilegios, puerto interno alto, sistema de archivos de solo lectura donde sea viable, directorios temporales limitados, límites de procesos y memoria, y capacidades retiradas. Las excepciones necesarias para Apache/PHP se justificarán con una prueba de arranque. No se supondrá que una imagen oficial funciona bajo cualquier endurecimiento sin validarlo.

Las imágenes y pesos se obtienen durante la preparación. La ejecución docente trabaja en redes internas. Los lanzadores del anfitrión podrán cambiar perfiles/imágenes sin exponer la administración de Docker a una estación del alumno. Los controles no dependerán de editar una variable del navegador.

## Método práctico y avance propuesto

Cada objetivo siguiente es una especificación para desarrollo, no una función actual del juego.

| Desafío propuesto | Pasos del estudiante | Condición de aceptación que se implementaría |
|---|---|---|
| 1. El permiso del cliente | Leer función, datos, destinos y acciones admitidas. Escribir una predicción y detención observable | Alcance guardado y episodio vigente. La calidad del fundamento requiere revisión docente |
| 2. El aviso correcto | Separar las dos CVE y localizar condiciones en avisos primarios | Referencias existentes, condición y CVE coherentes, fecha conservada |
| 3. Dos PHP distintos | Consultar CLI y operación web controlada. Identificar SAPI, compilación e imagen que atiende | Observación obtenida del servicio real y metadatos verificados del despliegue. El banner por sí solo no basta |
| 4. La línea base | Ejecutar transacción sintética legítima y prueba acotada seleccionada | Ambas con correlación, episodio, versión, método y resultado. Una prueba fallida queda fallida |
| 5. La falsa solución | Comparar la medida parcial del dossier con las condiciones de ambos avisos | Distinguir mitigación de corrección y conservar el residual. No conceder cierre global por una configuración |
| 6. El plan del dueño | Elegir actualización, restricción temporal u otra acción sustentada | Función, alternativa, responsable, riesgo del cambio y criterios de aceptación/reversión |
| 7. El despliegue real | Aplicar el cambio mediante una operación permitida del laboratorio | Imagen/paquete fijados y trabajadores activos identificados después del cambio, sin usar un socket Docker desde el target |
| 8. La contraprueba | Repetir la prueba de seguridad y la función legítima | Nuevas observaciones posteriores a la intervención, mismo objeto e identidad cuando corresponda, control actual aplicado |
| 9. El asistente bajo examen | Solicitar borrador local con fuentes delimitadas. Revisar una afirmación completa | Inferencia real auditada, referencias válidas y decisión humana que explique respaldo y límite |
| 10. El expediente | Defender estado, tratamiento, residual y obligación aplicable | Cadena de evidencias completa. Propuesta del dueño separada de automatismos, sin envío externo |

En la interfaz, cada paso mostrará una única acción principal, la pregunta que resuelve y la evidencia que falta. Las tareas técnicas mantendrán guías para noVNC y SSH. Los formularios de juicio y la revisión humana seguirán siendo necesarios.

## Qué prueba se incorporará

El desarrollo tendrá dos niveles que se nombrarán de forma diferente:

1. **Verificación de gestión y regresión.** Siempre disponible con las imágenes construidas: inventario preciso, proceso web, configuración, despliegue, función legítima y prueba de regresión benigna pertinente a la corrección. El expediente distinguirá una prueba de código del proyecto, una prueba HTTP y una medición del servicio. Una prueba interna del motor PHP no acredita por sí sola exposición de toda la aplicación.
2. **Reproducción técnica de la vulnerabilidad, si se valida.** Solo se incorporará después de revisar procedencia, código, dependencias, condiciones, SAPI, arquitectura y efecto reproducible de la prueba elegida. Tendrá un objetivo benigno fijo dentro del contenedor, con salida y correlación verificadas. No requerirá consola libre, Internet, datos reales ni persistencia. No se publicará un resultado exitoso que todavía no se haya observado.

La ausencia de reproducción en una configuración se registrará como resultado de esa prueba. No se usará para declarar «no afectado» ignorando el aviso y la distribución. Tampoco se sustituirá por un marcador artificial presentado como explotación auténtica. Si el nivel 2 no alcanza calidad suficiente, la misión seguirá enseñando tratamiento y verificación del nivel 1, con el límite explícito.

Un repositorio de PoC recién aparecido se tratará como material no confiable hasta revisión. Se conservarán licencia, commit y análisis de lo que ejecuta. La compilación de una imagen o un resultado reproducido en AMD64 no acreditarán automáticamente ARM64.

## Evidencia mínima del cambio

- Identidad de campaña, episodio y ejecución del target.
- Imagen y digest o compilación verificable, junto con la arquitectura.
- Versión del proceso web, SAPI, configuración pertinente y evidencia de trabajadores activos después del despliegue.
- Solicitud y respuesta de la función legítima antes y después.
- Método de seguridad, versión de la prueba, resultado y límite de lo que demuestra.
- Evento de intervención y observaciones posteriores, sin reutilizar un éxito anterior como continuidad posterior.
- Aviso primario utilizado, revisión, condiciones, distribución y posibles backports.
- Dueño, responsable, tratamiento, incertidumbre, residual y revisión.

Un hash ayuda a conservar el archivo. El verificador también debe contrastar su origen y contenido. La comprobación de avance heredará el vínculo con la sesión activa y no aceptará pruebas de una campaña anterior. El control actual deberá concordar con la evidencia del cierre.

## IA local con una pregunta evaluable

Se reutilizará el modelo pequeño actual como referencia inicial, sin presumir que resuelve correctamente el caso. Recibirá fragmentos identificados de avisos y evidencias sintéticas. Una nota sintética de proveedor mezclará condiciones o afirmará que actualizar el CLI basta para cerrar, siempre etiquetada en la guía docente como material del ejercicio.

El alumno comparará afirmaciones con fuentes. Se medirán referencias inventadas, condiciones omitidas, conclusiones excesivas y correcciones humanas. La comparación manual/IA tendrá las mismas preguntas y datos. El resultado no será una afirmación genérica de que «usar IA ahorra tiempo»: deberá mostrar utilidad y costo de revisión sobre esta tarea.

Una segunda variante contendrá una instrucción adversaria dentro de un documento sintético, vinculada al módulo de evaluación del asistente. El texto recuperado no podrá modificar permisos ni invocar cambios. Se comprobará el límite fuera del modelo. RAG, JSON o un prompt más largo no se presentarán como garantía de que la inyección desaparece. Referencia: [OWASP, inyección de instrucciones](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

## Riesgo, ATT&CK, ISO y Chile

La misión conservará el índice ordinal del curso `R = 4 × L × I máximo`, con niveles y vector de impactos justificados por el dueño. Comparará el mismo hallazgo técnico en portal de transferencia, aplicación administrativa aislada y función esencial ficticia. No multiplicará CVSS, EPSS e impacto como si fueran unidades compatibles.

[T1190](https://attack.mitre.org/techniques/T1190/) será candidata si la conducta y el borde simulado la sustentan. No se agregará T1078 sin uso observado de una identidad pertinente ni T1486 por la reputación de un actor. La observación histórica y el estado del control conservarán campos diferentes.

Como referencias orientativas se podrán estudiar A.8.8, A.8.9, A.8.26 y objetivos pertinentes de continuidad y registro de [ISO/IEC 27001](https://www.iso.org/standard/27001). El mapeo necesitará razón y prueba. No acreditará certificación ni cobertura universal.

La condición OIV se entregará como supuesto del cliente ficticio. La existencia de una versión afectada no se transformará automáticamente en un incidente significativo. Si una tarjeta añade hechos de incidente, se aplicará el análisis de [Ley 21.663](https://www.bcn.cl/leychile/navegar?i=1202434) y [D.S. 295](https://www.diariooficial.interior.gob.cl/publicaciones/2025/03/01/44088/01/2617387.pdf), conservando fecha del caso, vigencia, efecto y bases de reporte. Los borradores permanecerán locales.

## Presupuesto inicial para 16 GB sin GPU

Se medirá en un equipo de referencia antes de prometer compatibilidad. Esta tabla es un **presupuesto de diseño**, no una medición realizada:

| Perfil | Componentes adicionales activos | Objetivo inicial de memoria adicional |
|---|---|---|
| Inventario y cambio PHP | Un target, gateway y verificador ligero | Hasta 768 MiB sobre la base necesaria |
| Comparación pre/post | Targets alternados y evidencia persistente | Mantener un único target activo cuando sea posible |
| Revisión IA | Target mínimo y Ollama existente | Reutilizar el límite actual del motor, sin sumar otro modelo |
| ZAP opcional | Perfil pasivo ya existente | Detenerlo al inferir o compilar si el equipo lo necesita |

Los límites de memoria, CPU, procesos, solicitudes y archivos temporales serán parte de la configuración. No se sumará una nueva plataforma pesada para esta misión. El tamaño de las imágenes, espacio temporal de compilación y almacenamiento del modelo también deben medirse. Una compilación que exceda el equipo se resolverá preparando imágenes verificadas, conservando receta y procedencia.

El perfil PHP sustituirá al perfil ZAP de 768 MiB mientras esté activo. Con el presupuesto propuesto de hasta 768 MiB para target e instrumentación adicional, la suma declarada podrá mantenerse dentro de los 7744 MiB del perfil actual completo, en lugar de añadir ambos simultáneamente. El lanzador deberá impedir combinaciones que superen el presupuesto de Docker y conservar margen para el anfitrión. Esto es un criterio de diseño que debe medirse, no una garantía ya validada.

## Criterios para pasar de propuesta a laboratorio público

1. Elegir una rama, pareja de compilaciones y SAPI con avisos revisados. Verificar etiquetas/digests disponibles antes de escribir instrucciones que dependan de ellos.
2. Construir la operación sintética y comprobar aislamiento desde anfitrión, análisis y aplicaciones.
3. Reproducir la discrepancia real entre artefacto disponible y proceso activo sin falsificar versiones.
4. Seleccionar y revisar las pruebas del nivel 1. Habilitar el nivel 2 solo con reproducción verificada y documentada.
5. Implementar comprobadores del episodio, evidencias actuales y continuidad posterior. Intentar engañarlos con archivos editados, eventos antiguos y un servicio apagado.
6. Probar recorrido completo por noVNC y por SSH, reanudación de campaña y recuperación ante una herramienta no disponible.
7. Pilotar AMD64 y ARM64, un equipo físico de 16 GB sin GPU y el lanzador Windows. Publicar límites observados.
8. Revisar la guía con principiantes: predicción, acción, resultado, explicación, pista progresiva y contraprueba en cada objetivo.

La misión estará lista cuando un estudiante pueda defender **qué proceso cambió, qué efecto dejó de observarse, qué función siguió funcionando y qué riesgo conserva el dueño**. Obtener una consola por sí solo no será el criterio de logro.
