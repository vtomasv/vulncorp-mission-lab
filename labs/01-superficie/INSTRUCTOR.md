# Instructor · Clase 1

Guía pública: no contiene un examen ni depende de ocultar respuestas. [Agenda y pasos](ESTUDIANTE.md).

## Preparación

Ejecutar `./lab.sh up` y `./lab.sh smoke`; después dejar targets iniciales y advertir que smoke agregó evidencia de verificación. Para una clase limpia, usar otro nombre de proyecto/volumen, sin borrar el trabajo de un alumno. No ejecutar limpieza global de Docker.

## Secuencia y preguntas

| Bloque | Intervención docente |
|---|---|
| Activación 20 | No mostrar Hallazgos. Pedir tres predicciones sobre alcance y dependencia. |
| Conceptos 40 | En principiantes usar una imagen, un contenedor y un puerto real del caso. Diferenciar red del host y red del contenedor. |
| Demo 30 | Mostrar una transacción, su evidencia y una conclusión limitada. No resolver la exposición antes del laboratorio. |
| A 110 | Primeros 30 min con terminal guiada; después comparar public/support. El auditor debe preguntar «¿desde dónde?». |
| B 110 | Validar export/diagnostics; entrevistar al dueño. Un dato técnico no sustituye consecuencias. |
| Comité 80 | Presentación de tres investigaciones; tarjeta de giro; otra persona impugna una afirmación. |
| Cierre 30 | Reflexiones individuales y exportación, sin nota. |

## Respuestas y errores esperables

- Hay tres targets; mission es plano de gestión. El número de contenedores puede aumentar temporalmente por sondas o IA.
- La sonda public alcanza gateway. La sonda support alcanza backup. Ambas tienen alcance fijo de tres targets y excluyen mission.
- records es alcanzable por gateway desde app; no directamente desde esas dos sondas. Un error de resolución no prueba inexistencia.
- Export devuelve datos sintéticos sin autenticación. Diagnostics revela topología. Ninguno demuestra una consola ni acceso general a las redes.
- La cuenta compartida de backup tiene un catálogo que declara permisos; no se implementa borrado. No premiar afirmaciones exageradas.
- Salud: resultados urgentes y capacidad manual limitada. Agua: recuperación de telemetría y ausencia de relación del portal con dispositivos físicos. Digital: API compartida entre clientes.

Si un grupo termina antes, pedir una prueba que refute su propia hipótesis; no aumentar simplemente el número de comandos.

## Ayudas

1. Pregunta «¿la ruta que dibujaste es TCP directo o una petición que reenvía la aplicación?».
2. Mostrar `probe public transaction` y pedir revisar gateway → records.
3. Acompañar `compose.yaml`, con las redes de cada servicio.

## Criterio formativo

Escuchar si la persona puede distinguir observación de inferencia y unir activo, servicio y dueño. El checkbox o la longitud de una reflexión no acreditan por sí solos aprendizaje.
