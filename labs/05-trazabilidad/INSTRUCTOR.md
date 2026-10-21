# Trazabilidad · guía docente

Esta zona busca que la evidencia determine el relato. El núcleo técnico debe realizarse en orden: simulación, cronología, mapeo, ensayo previo, autorización, ensayo posterior, revocación, ensayo posterior y capa. El agente impide cambios adelantados y pide una línea base de tres identidades antes de cada control.

## Discusión conceptual previa

Explicar táctica, técnica y procedimiento con una sola solicitud del caso. Distinguir observación, hipótesis y ausencia de visibilidad. Después presentar una cadena exagerada que incluya cifrado y pedir que el grupo identifique qué eslabones no tienen prueba. Nunca presentar un heatmap como demostración automática de detección o de cumplimiento.

El T1078 del ejercicio depende del supuesto explícito del guion: una credencial declarada comprometida se usa para su cliente permitido. La solicitud no demuestra su robo. El mapeo T1190 corresponde al abuso simulado de la aplicación por gateway. Las versiones individuales se fijan en el expediente; no se atribuye una versión de toda la matriz ATT&CK sin incorporar esa base.

## Cómo sostener una jornada intensiva

La ejecución guiada es una base relativamente breve. Ampliar con lectura de fuente primaria, reconstrucción causal de registros de dos procesos, matriz de visibilidad, contrapruebas de ambos clientes, revisión entre pares de capas y defensa al dueño. El entregable central es la trazabilidad de la conclusión, no memorizar IDs ni repetir un comando durante horas.

Rotar los papeles de analista, responsable de servicio y auditor. Pedir al dueño que acepte o rechace un criterio de continuidad, y al auditor que identifique una inferencia no demostrada. No hay calificaciones intermedias; las discrepancias deben provocar una nueva prueba o una limitación explícita.

## Evidencias mínimas y contrapruebas

| Punto | Debe conservarse | No aceptar como sustituto |
|---|---|---|
| Cronología | Tres IDs del último SIM, orden local y correlación | Una historia redactada sin registros |
| Mapeo | Un evento distinto para cada conducta | CVE o color de herramienta |
| Autorización | Tres solicitudes antes, cambio confirmado y tres después | Solo un 403 o un control solicitado sin respuesta |
| Revocación | 401 de la llave comprometida + 200 legítimo + 403 entre clientes | Bloquear todas las identidades |
| Capa | JSON con técnicas, IDs, análisis y episodio | Un dibujo sin procedencia |

Pedir que otro equipo quite mentalmente una fuente y explique qué conclusión deja de sostenerse. Esto revela dependencia real de evidencia, incluso cuando ambos equipos ya obtuvieron PX.

## Límites operativos

Los controles y registros del nuevo rango persisten en `range_state`, incluso al recrear contenedores. Una campaña nueva genera otro episodio y no puede reutilizar fuentes del anterior. El historial central también persiste. No borrar volúmenes ni reiniciar todo el curso para solucionar un error de selección en la UI.

La capa es un formato de intercambio compatible, no una instancia completa de Navigator ni una afirmación de cobertura. El laboratorio registra y previene lo que sus pruebas comprueban; no incluye un SIEM ni una regla de detección real. Las PPT posteriores deben explicar esa diferencia.
