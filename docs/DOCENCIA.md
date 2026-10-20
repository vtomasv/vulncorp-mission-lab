# Plan docente · clases 1 a 3

## Preparar una experiencia, no una instalación colectiva

Antes de dictar, ejecutar `doctor`, `up`, `sbom`, `scan` y `ai-prepare` en los equipos de práctica. Las descargas son preparación técnica, no trabajo académico calificable. Conservar cachés y reporte real con fecha. Probar las guías con una persona principiante: el instructor experto no es una medida suficiente de duración.

Se necesitan Git y Docker; todo el resto corre en contenedores. Para 16 GB/CPU usar Qwen3 1.7B y alternar perfiles. No levantar plataformas pesadas de gestión ni modelos 8B en estas tres jornadas. El centro de misión es el registro del proceso, no un simulacro de un producto comercial.

Cada guía reserva 420 minutos efectivos y pausas aparte. Solo el examen final del curso genera nota; estas actividades no aportan puntos, bonos, rankings ni penalizaciones. Los contadores indican reflexiones guardadas, no competencia certificada.

## Trabajo cognitivo visible

En cada bloque de laboratorio pedir cuatro actos:

1. **Predecir** antes del comando.
2. **Observar** sin sustituir el resultado por lo esperado.
3. **Explicar el límite** de lo observado.
4. **Cambiar una premisa** y revisar la decisión.

Grupos de 3-4; rotación de roles cada 20-30 minutos. Nadie queda toda la clase como espectador del teclado. Cada persona registra una explicación breve propia al cierre. El grupo puede compartir pruebas; no debe sustituir el razonamiento individual.

## Cómo retirar ayudas

| Clase | Ayuda disponible | Decisión que no se entrega resuelta |
|---|---|---|
| 1 | Lanzador, salida esperada, glosario y rutas de recuperación. | Dependencia relevante y pregunta al dueño. |
| 2 | Reporte proveedor, advisory y comparación de imágenes. | Aplicabilidad y clasificación con evidencia. |
| 3 | Formulario, motor de cálculo, tabla oficial SSVC y referencia docente desplegable. | Valores de contexto, urgencia, cartera y aceptación. |

**Error productivo 1:** un equipo dice que records no existe porque no resuelve desde edge. Pedir la transacción y otra perspectiva de red.

**Error productivo 2:** un equipo cierra F-01 porque la biblioteca no se importa. Pedir una conclusión proporcional: componente afectado presente, sin ruta demostrada bajo la revisión realizada.

**Error productivo 3:** la IA cita un ID real pero el fragmento no sustenta la conclusión. Preguntar qué parte de la frase está realmente respaldada.

**Error productivo 4:** se obtiene HTTP 403 después de un control y se cierra el caso sin verificar negocio. Pedir transacción legítima y explicar la causa raíz pendiente.

## Conexión con el programa

- Identificación/manejo: inventario, taxonomías, alcance y consecuencias.
- Metodologías: hipótesis, reglas de prueba, evidencia y reporte; no se evalúa memorizar listas de fases.
- ATT&CK: T1190/T1213.006/T1078 como candidatos según conducta y contexto. Un CVE no se mapea automáticamente a una técnica.
- Remediación: negociación, control temporal, prueba de seguridad y función, riesgo residual.
- IA: uso local auditable, sin autoridad para cerrar hallazgos ni ejecutar comandos.

Las clases 1-3 preparan los laboratorios posteriores de validación profunda y recuperación. Aquí se comprueba catálogo y continuidad de una transacción; no se afirma haber probado restauración, SQL injection de Django, ransomware ni movimiento lateral.

## Evidencias formativas

Una buena entrega tiene pocas afirmaciones sólidas: archivo de inventario o dibujo, dos perspectivas de acceso, SBOMs de imágenes distintas, reporte real con procedencia, clasificación razonada, decisiones para dos clientes, revisión IA y comparación antes/después de un control.

El expediente JSON incluye solo lo registrado en el centro de misión. Los archivos CLI/SBOM/Grype se conservan aparte en `artifacts/`; el alumno los adjunta a su carpeta de laboratorio. No se solicitan datos personales reales ni credenciales del equipo.

Guías del docente por jornada: [Clase 1](../labs/01-superficie/INSTRUCTOR.md), [Clase 2](../labs/02-evidencia/INSTRUCTOR.md), [Clase 3](../labs/03-priorizacion/INSTRUCTOR.md).
