# Gobierno · guía docente

Resultado esperado: un expediente que separe hechos técnicos, antecedentes del dueño, inferencias, obligaciones aplicables y decisiones pendientes de autoridad. No se califica; solo el examen final del curso tiene nota.

## Preparación y alcance jurídico

Preparar motor y pesos locales con el mismo lock utilizado en el tramo anterior. Leer fuentes primarias a la fecha de impartición: Ley 21.663, Reglamento de reporte (DS 295/2024, publicado el 1 de marzo de 2025), Ley 21.459 y normativa de datos aplicable a la fecha del caso. La referencia docente se verificó el 21 de octubre de 2026. No convertir este ejercicio en una certificación ni en un envío real.

La OIV es una condición explícita del guion, no una calificación automatizada. Los efectos sobre resultados urgentes son antecedentes sintéticos del negocio. Se observan solicitudes y controles; no se observan daño clínico, robo real de credenciales ni restauración de copias. Conservar estas distinciones en todos los borradores.

## Pauta de cálculo para discusión

| Campo | Instante UTC |
|---|---|
| Alerta temprana A | 2026-10-21 15:00 |
| Actualización A: OIV y servicio esencial afectado | 2026-10-22 12:00 |
| Actualización B: sin afectación de función esencial | 2026-10-24 12:00 |
| Adopción máxima del plan de acción OIV | 2026-10-28 12:00; informar al adoptarlo |
| Final desde alerta enviada a las 14:00 | 2026-11-05 14:00 |
| Final D desde gestión del 7 noviembre a las 16:00 | 2026-11-22 16:00 |

La regla de 24 h requiere ambas condiciones. La confidencialidad y el acceso no autorizado pueden producir efecto significativo aunque el servicio continúe: B no queda fuera por falta de interrupción. Si el incidente sigue en curso al vencer el final, corresponde informe de situación y luego el final desde gestión. No sumar quince días desde la actualización. No trasladar estos vencimientos a un SLA de parcheo.

## Pauta de matriz y excepción

F-01/F-05: presencia e investigación de aplicabilidad, A.8.8. F-02: mitigación HTTP anterior, causa raíz pendiente, A.8.26. F-03: catálogo no acredita restauración, A.8.13. F-04: exposición de configuración, A.8.9; no demuestra movimiento lateral. Pedir el deber concreto del art. 8 pertinente a cada relación y la prueba que permitiría evaluar su eficacia. Los artículos legales y controles ISO no son intercambiables.

Los selectores de la plataforma son una pauta acotada del caso, no la única clasificación posible en todas las organizaciones. Si un equipo propone otra asociación defendible, discutirla y registrarla en el fundamento: los PX no evalúan toda esa interpretación. Evitar tratar un identificador de control como un certificado de cumplimiento.

La excepción es una propuesta con autoridad, alcance, vencimiento, revisión y disparador. La regla de 30 días es política ficticia. Pedir que el dueño explique qué tolera y qué rechaza. Si una nueva evidencia demuestra uso del componente legacy afectado, la decisión debe reabrirse: no basta con que la fecha de excepción aún no venza.

## Trabajo cognitivo intensivo

Después de la explicación teórica y el núcleo guiado, organizar una reunión simulada: el analista entrega expediente, el dueño cuestiona efecto en la función, el responsable de privacidad exige minimizar datos y el auditor intenta refutar una conclusión. Introducir B y D para obligar a recalcular y cambiar el tipo de reporte. Cada estudiante conserva su propio razonamiento.

Pedir dos versiones de un mismo párrafo: la que mezcla antecedentes del guion con mediciones, y su corrección con fuentes y límites explícitos. Comparar después con la síntesis del modelo. La IA se usa para mejorar redacción y detectar omisiones; la discusión humana decide si una afirmación es proporcional.

Si el taller guiado termina rápido, profundizar en el contraste de fuentes, revisión de los cuatro borradores, condiciones de excepción y defensa entre pares. No llenar la jornada repitiendo solicitudes. La teoría y los casos documentados deben preparar el taller; las PPT se desarrollarán sobre estos resultados después de validarlos.

## Cierre del expediente

Comprobar que la exportación contiene `lab_event`, `lab_record`, consulta local, fuentes, digest y revisión. El hash exportado acredita integridad del contenido bajo la serialización documentada, no autenticidad frente al dueño administrador del host. Los recibos firmados protegen la evidencia en la operación normal del alumno; esto no es una plataforma de examen resistente al administrador de Docker.
