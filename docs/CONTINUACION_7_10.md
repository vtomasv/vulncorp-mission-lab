# Continuación docente 7–10 · de la alerta al servicio defendible

La campaña tiene **10 zonas y 57 objetivos**. Se agregan 24 objetivos conservando los 33 anteriores. Cada zona nueva tiene seis desafíos. La interfaz sigue mostrando una misión a la vez, sin clases, duraciones ni entregas con nota. Los laboratorios son formativos; existe un único examen final.

| Taller | Zona del juego | Resultado defendible |
|---|---|---|
| 7 | Audita al asistente | Hipótesis propia, comparación de dos inferencias reales, revisión de fuentes y prueba de la frontera de autoridad. |
| 8 | Cambia el servicio real | CLI candidato frente a web activo, línea base, mitigación parcial, plan del dueño y cambio de runtime con función conservada. |
| 9 | Recupera la operación | Reapertura por deriva, priorización del nuevo contexto, copia real, interrupción sintética y restauración con hash. |
| 10 | Defiende el expediente | Transferencia a otro dueño, contraprueba, índice justificado, mapeos con alcance, revisión asistida y defensa humana. |

## Preparar antes de explicar el taller

El contenido teórico debe presentar fuente y confianza; condiciones de aplicabilidad de una CVE; diferencias CLI/SAPI/proceso web; tratamiento temporal frente a corrección; criterios de aceptación y reversión; riesgo del servicio y autoridad del dueño; copia frente a restauración; métricas con denominador y límite. Después se presenta el caso real y se abre el laboratorio. Las PPT correspondientes se construyen a partir de estas prácticas verificadas.

La preparación técnica es `up`, `php-on` y `ai-on`, después de descargar una vez los pesos mediante `ai-prepare`. Los comandos tienen equivalentes PowerShell. `php-on` detiene ZAP, levanta dos imágenes PHP y conserva los volúmenes. `webscan-on` detiene ambos PHP. No ejecutar perfiles de escáneres de imágenes adicionales durante una inferencia. Los lanzadores ordenan la preparación; la resolución de cada objetivo ocurre desde aplicaciones por noVNC o SSH.

Presupuesto con IA y PHP: **7360 MiB** de límites de contenedor, más sobrecarga del motor; con IA y ZAP: **7744 MiB**. La referencia sigue siendo equipo físico de 16 GB, Docker con 8 GiB, sin GPU, un modelo y una inferencia a la vez. Es un presupuesto, no una garantía de consumo máximo ni un piloto físico ya realizado. Las dos bases PHP añaden descargas y espacio; conservar al menos 40 GB libres recomendados para el conjunto.

## Caso PHP2Shell: alcance implementado

Se implementa el **nivel 1 de la propuesta**: comparación de versiones y despliegues reales, identidad del runtime web y regresión funcional. Las dos imágenes oficiales están fijadas por digest en `data/php-images.json`: PHP **8.4.26** y **8.4.27**, ambas Apache/mod_php. El comando de inventario ejecuta de verdad el CLI de la candidata y consulta por HTTP el runtime activo antiguo. No fabrica una discrepancia de versiones.

La petición multipart es pequeña y benigna. No reproduce RCE, no carga una webshell ni constituye el PoC de CVE-2026-109618 o CVE-2026-109619. Un 200 prueba el resultado funcional descrito; no demuestra explotación ni que el sistema carezca de vulnerabilidades. Las condiciones y limitaciones de cada aviso se analizan por separado en [las fuentes](FUENTES_7_10.md).

`php-mitigar` restringe la sonda multipart en la frontera del controlador. La respuesta 415 queda identificada como bloqueo anterior a PHP; la versión antigua no cambia. Es una medida parcial para esta ruta. `php-desplegar` cambia la ruta hacia el contenedor corregido ya precargado y retira esa restricción. No recompila ni reinicia todos los procesos antiguos: el contenedor antiguo queda aislado para el ejercicio posterior de reversión. No presentar esta retención como una política adecuada de producción.

## Misiones y trabajo cognitivo

**Asistente.** El alumno conserva primero una hipótesis y una condición que la refutaría. Después compara dos consultas reales: avisos primarios resumidos y los mismos avisos más una nota ficticia con órdenes incrustadas. El modelo puede resistir la nota; la progresión no exige una respuesta dañina. Se inspeccionan fuentes recibidas, salida, digest, esquema y estado antes/después. No se le entregan herramientas de ejecución ni autoridad de aceptación.

**Remediación.** El alumno compara versión, SAPI, digest, identidad y función. Formula un plan con el dueño antes de cambiar. El cierre exige runtime corregido real, documento completado y prueba posterior al cambio. Repetir una observación antigua o completar solo el formulario no satisface esos requisitos. La regresión protege la función del cliente, sin exagerar lo probado sobre las CVE.

**Operación.** Una reversión real de ruta vuelve a servir el runtime antiguo. La historia conserva PX y evidencias, pero el nuevo objetivo exige evidencia actual. El cambio de impacto del dueño es ficticio y se identifica como tal. Se aplica la política ordinal `4×L×máximo impacto`; el vector de deriva 5/2/5/4 con L=4 da 80 antes de atribuir reducción de L al tratamiento. Se crea una copia real, se altera solo el documento sintético, se observa 503 con el proceso sano y se restaura el contenido con el hash conservado. El intervalo medido corresponde a dos observaciones del ejercicio, no al RTO ni a la duración completa del incidente.

**Defensa.** ArchivoSur cambia función, alternativa y dueño, conservando el mismo portal de práctica. El alumno elige y justifica su vector residual; el backend comprueba la aritmética de su índice, sin decidir la legitimidad del vector. Se distingue T1190 como amenaza hipotética de conductas realmente observadas. Las referencias A.8.8, A.8.13 y marco OIV orientan la gestión; no acreditan cumplimiento. Una tercera inferencia incorpora un evento actual y vuelve a requerir dictamen humano. El expediente se exporta antes y después de la defensa para incluir la última decisión.

## Exigencia sin depender de esperas

Las acciones cortas dejan espacio para trabajo profesional, no para repetir comandos. Pedir siempre predicción, evidencia concreta, alternativa rechazada, contraprueba y autoridad del dueño. Intercambiar roles de analista, dueño, proveedor y revisor. Un revisor debe formular una objeción verificable y el equipo responder con un evento de la revisión pertinente.

Si el grupo avanza rápido: comparar dos vectores legítimos de impacto para el mismo portal; identificar qué observaciones se reutilizan con otro dueño; proponer qué prueba falta para hablar de recuperación integral; revisar una conclusión de IA con cita válida pero alcance excesivo; reconstruir una decisión sin abrir el tablero del compañero. El docente profundiza criterio y trazabilidad sin añadir calificaciones intermedias.

La defensa de esta campaña es un ensayo público. El único examen final usa otro expediente, preparado fuera del repositorio público, con función, evidencias y supuestos distintos pero habilidades ya practicadas.

## Guías

- [Audita al asistente](../labs/07-asistente/ESTUDIANTE.md).
- [PHP2Shell y remediación](../labs/08-php2shell/ESTUDIANTE.md).
- [Operación y recuperación](../labs/09-operacion/ESTUDIANTE.md).
- [Defensa del expediente](../labs/10-defensa/ESTUDIANTE.md).
- [Validación reproducible y limitaciones](VALIDACION_7_10.md).
