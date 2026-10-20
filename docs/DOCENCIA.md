# Tres jornadas de siete horas; una campaña continua

La interfaz del jugador habla de zonas y objetivos. La organización académica vive en estas guías: no se transforma cada jornada en un menú del producto. Esta edición usa tres zonas y quince objetivos; el curso completo puede prolongar la misma campaña.

Solo el examen final del curso genera nota. Los PX son hitos de práctica sin ponderación, bonos ni penalización. El tablero comprueba evidencias técnicas y restricciones; no certifica comprensión ni califica automáticamente el criterio.

## Preparación docente

Ejecutar `prepare-game` antes de la jornada; comprobar noVNC, SSH, Grype e inferencia en cada equipo. Precargar imágenes, base y pesos. Probar las guías con una persona principiante y registrar tiempos: no hay todavía piloto físico de 16 GB ni validación de duración en una cohorte.

Cada estudiante dispone de su instalación. Se puede discutir en tríos, rotando analista, dueño y auditor cada 25 minutos, pero cada persona opera su puesto y conserva sus decisiones. El curso no requiere instalar herramientas de seguridad en el host.

## Distribución de cada jornada

420 minutos de reloj: 380 de trabajo y 40 de pausas incluidas:

| Bloque | Min | Terreno | Señales | Continuidad |
|---|---:|---|---|---|
| Predicción | 20 | Dibujar la cadena del servicio. | Anticipar qué puede y qué no puede decir un escáner. | Proponer una prioridad sin conocer todavía el dueño. |
| Conceptos esenciales | 35 | Servicio, dependencia, exposición y evidencia. | Identidad del activo, SBOM, CVE, alias y aplicabilidad. | Índice ordinal, SSVC, controles y responsabilidad. |
| Demostración breve | 25 | Teclado, noVNC, prompt y lectura de una respuesta. | Procedencia, archivo real y revisión de imports. | Un cálculo y una revisión crítica de una afirmación IA. |
| Pausa | 10 | Recuperación. | Recuperación. | Recuperación. |
| Juego y contraste I | 100 | Objetivos 1–3; probar predicciones y explicar límites. | Objetivos 6–8; explorar paquetes, advisories y código. | Objetivos 11–12; entrevistar dueños, comparar y revisar IA. |
| Pausa | 20 | Descanso. | Descanso. | Descanso. |
| Juego y contraste II | 100 | Objetivos 4–5; reproducir exposición y cambiar de perspectiva. | Objetivos 9–10; impugnar el proveedor y defender el expediente. | Objetivos 13–15; negociar cartera, mapear y probar medida/función. |
| Pausa | 10 | Recuperación. | Recuperación. | Recuperación. |
| Defensa y contraprueba | 70 | Reconstruir red, dependencia y preguntas al dueño. | Otro equipo intenta refutar tres conclusiones usando las fuentes. | Otro equipo cuestiona alcance del control, residual y aceptación. |
| Reflexión y expediente | 30 | Una observación, una inferencia y una pregunta pendiente. | Una alerta descartada de prioridad, pero conservada con sus límites. | Qué decisión cambió y qué nunca delegaría al modelo. |

No se llenan siete horas copiando quince comandos. Los hitos son la columna vertebral de una investigación: cada bloque incluye predicción individual, ejecución, contraste en pareja, revisión de evidencia y defensa. Los equipos rápidos realizan contrapruebas, no esperan bloqueados por temporizadores.

## Profundizar con trabajo real

**Terreno:** antes de `lab red`, cada persona predice una matriz puesto/servicio. Después compara DNS y TCP, localiza la dependencia que no era visible desde análisis y explica por qué `completed` no demuestra autorización. En soporte, distinguir acceso al catálogo de restauración probada. Cambiar el dueño y preguntar qué función es esencial.

**Señales:** abrir `~/evidence/records.cdx.json`, localizar purl y versión con jq, confrontar el advisory del proveedor y leer `/company/active-service/targets.py`. Registrar por separado hecho, hipótesis, alcance y fuente. No convertir «no importa Django en este archivo» en «jamás puede usarse». Proponer una prueba que podría invalidar la clasificación.

**Continuidad:** mantener el hecho técnico y L al comparar salud/agua; explicar qué consecuencias cambian. Discutir el máximo de impactos y los límites de operar escalas ordinales. Revisar las definiciones de Human Impact antes de SSVC. En IA, identificar una frase completa, verificar su fragmento y corregir una inferencia no sustentada. Defender qué tratamiento queda pendiente con 4 h/15 min y distinguir ruta HTTP de segregación de redes.

## Retirada progresiva de ayudas

La guía muestra ubicación, comando, razón y pistas. Primero se exige predecir antes de desplegar la pista; después se pide formular una contraprueba antes de ejecutar el siguiente paso. Las pistas no restan puntos. Los ejemplos de respuesta del instructor orientan discusión, no son una pauta de aceptación universal del riesgo.

Errores productivos: confundir DNS con inexistencia; presencia con explotación; CVSS con prioridad del dueño; referencia IA válida con conclusión sustentada; 403 con continuidad; asociación normativa con cumplimiento. Pedir siempre **qué viste, qué infieres y qué todavía no puedes afirmar**.

Guías: [Terreno](../labs/01-superficie/ESTUDIANTE.md), [Señales](../labs/02-evidencia/ESTUDIANTE.md), [Continuidad](../labs/03-priorizacion/ESTUDIANTE.md). Los recursos del instructor acompañan cada una. La ampliación se rige por [el diseño de campaña](REPLANTEAMIENTO_JUEGO.md).
