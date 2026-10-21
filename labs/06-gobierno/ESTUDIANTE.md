# Responde ante el dueño

Tu trabajo no termina al bloquear una solicitud. Debes explicar qué función protege el control, quién responde por lo pendiente, qué evidencia conserva la organización y cuándo corresponde reportar un incidente. La empresa y su condición OIV son **supuestos ficticios**. Los borradores de este taller se guardan localmente y no se envían a ninguna autoridad.

## 1. El servicio tiene un dueño

Continúa la campaña después de la capa ATT&CK. Lee el contexto de **Red Salud Sur ficticia**: resultados urgentes, dependencia de la API y limitaciones del procedimiento alternativo. Identifica al dueño de la función y al responsable de coordinar la respuesta. El proveedor del escáner no sustituye esa autoridad.

En el objetivo de alcance, explica por qué la designación OIV no puede inferirse de Docker, del sector por sí solo ni de un CVSS. Aquí se entrega como supuesto para poder practicar las obligaciones del caso. Distingue un hecho medido del rango de un antecedente aportado por el dueño ficticio.

## 2. Del hallazgo a la obligación

La interfaz presenta una fila a la vez. Para F-01 a F-05 elige objetivo de control ISO 27001:2022, estado de la evidencia y marco de gestión. Cita en cada fundamento un ID existente, por ejemplo `EV-PACKAGES`, o el ID de una prueba auténtica del expediente. Los fragmentos docentes describen contexto: no los presentes como nuevas mediciones.

| Hallazgo del expediente original | Pregunta para razonar | Referencia orientativa |
|---|---|---|
| F-01 · Django presente | ¿Está presente, usado o explotado? ¿Qué dato falta? | A.8.8 · vulnerabilidades técnicas |
| F-02 · exportación sin autorización | ¿La restricción HTTP corrige la causa raíz en records? | A.8.26 · seguridad de aplicaciones |
| F-03 · llave compartida del catálogo | ¿Ver un catálogo acredita restauración? | A.8.13 · copias de seguridad |
| F-04 · diagnóstico expuesto | ¿La topología pública demuestra movimiento lateral? | A.8.9 · configuración |
| F-05 · requests presente | ¿Se demostró la condición de uso que exige el advisory? | A.8.8 · vulnerabilidades técnicas |

No confundas estos hallazgos con R-01/R-02 del nuevo rango. La ruta `/range/live` y `/api/export` son diferentes. El gemelo vulnerable sigue existiendo para aprender; no equivale a un despliegue productivo todavía expuesto.

Para cada fila completa esta cadena: **hecho → consecuencia para el dueño → objetivo del control → prueba disponible → prueba pendiente → responsable**. La Ley 21.663 art. 8 orienta el análisis del sistema de gestión y las medidas/revisiones del OIV ficticio. Una fila ISO completada no prueba cumplimiento integral; una CVE no acredita por sí sola un incidente significativo ni una técnica ATT&CK observada.

Los nombres de controles se usan como referencia resumida; no se reproduce el estándar ISO. Consulta la [referencia oficial](https://www.iso.org/standard/27001) y el ejemplar autorizado de tu organización para interpretar su alcance.

## 3. Una vulnerabilidad no basta

Desde aplicaciones:

```bash
lab incidente
cat ~/evidence/incidente-oiv.json
```

El archivo fija las horas y los antecedentes del negocio; no se inicia una cuenta regresiva personal. Distingue estos casos:

| Caso | Antecedente del ejercicio | Decisión que debes justificar |
|---|---|---|
| A | OIV ficticia, acceso entre clientes y afectación de función esencial según el guion | Preparar reporte simulado por efecto significativo y aplicar la regla especial de actualización |
| B | Acceso no autorizado a datos del guion, sin afectación de función esencial | Analizar efecto significativo por confidencialidad/acceso indebido; no exigir una caída para reportar |
| C | Paquete vulnerable presente, sin incidente demostrado por esa CVE | Gestionar vulnerabilidad e investigar; no inventar un incidente observado |
| D | Variante A aún en curso al vencer el informe final | Preparar informe de situación y calcular el final posterior a su gestión |

El retraso de resultados urgentes es un **antecedente simulado del negocio**: el rango no produce daño clínico ni mide una caída real del servicio. El acceso HTTP sí tiene eventos observados. Esta distinción debe aparecer en tus borradores.

## 4. El reloj empieza con un hecho

Consulta [Ley 21.663, art. 9](https://www.bcn.cl/leychile/navegar?i=1202434) y el [Reglamento, Decreto 295/2024](https://www.diariooficial.interior.gob.cl/publicaciones/2025/03/01/44088/01/2617387.pdf). Usa las horas del dossier, con zona horaria explícita:

- Conocimiento del caso: `2026-10-21T12:00:00Z`.
- Envío simulado de alerta temprana: `2026-10-21T14:00:00Z`.
- Variante D gestionada según el guion: `2026-11-07T16:00:00Z`.

`Z` significa UTC. Puedes usar un desplazamiento explícito equivalente; no ingreses una hora local sin zona. El formulario espera instantes, no «mañana» ni «en tres horas».

| Hito | Base de cálculo |
|---|---|
| Alerta temprana | Máximo 3 h desde conocimiento del incidente que pueda tener efecto significativo |
| Actualización general | Máximo 72 h desde conocimiento |
| Actualización especial | Máximo 24 h si concurren OIV y afectación del servicio esencial |
| Plan de acción OIV | Informar tan pronto se adopte; adopción hasta 7 días corridos desde conocimiento |
| Informe final | Hasta 15 días corridos desde el **envío de la alerta temprana**, no desde la actualización |
| Si sigue en curso | Informe de situación; final hasta 15 días desde que se haya gestionado |

Calcula los seis vencimientos solicitados. Después redacta cuatro borradores docentes: alerta, actualización, plan de acción y final. No son formularios oficiales ni sustituyen todos sus campos reglamentarios. Incluye informante ficticio, servicio afectado, instante de conocimiento, observación comprobada, antecedente del guion, incertidumbre y medidas verificadas. En el final explica causa y alcance sin inventar cifrado ni recuperación probada. Para D, explica qué sustituye al final inicial.

El cierre normativo no queda acreditado porque el analista pulse «conservar». El Reglamento define el incidente gestionado en relación con los antecedentes que permiten a la Agencia prescribir su cierre. La hora del caso D es un dato del guion para practicar el cálculo, no una decisión unilateral automática de la plataforma.

**Estos son plazos de reporte, no plazos universales de parcheo.** La gestión de una vulnerabilidad y el ciclo de respuesta a incidentes se relacionan, pero no se reemplazan.

## 5. Una decisión que vence

Propón una excepción para la investigación/actualización de los componentes legacy pendientes. No exceptúes como si siguiera abierta la falla R-01 que ya probaste como contenida en `live`.

Registra:

1. Dueño con autoridad y responsable del tratamiento.
2. Razón de negocio para el aplazamiento y supuesto que podría invalidarla.
3. Controles compensatorios con eventos actuales de bloqueo **y** acceso legítimo.
4. Vencimiento con zona horaria y fecha de revisión.
5. Disparador que revoca la excepción y acción a realizar.

La política ficticia limita esta propuesta a 30 días desde el conocimiento del caso. No es un plazo fijado por la ley. La plataforma conserva una **propuesta**; el modelo y los PX no aceptan riesgos en nombre del dueño.

## 6. El expediente vuelve a tus manos

Verifica que el motor IA y sus pesos ya estén preparados. Desde aplicaciones:

```bash
lab ia-expediente
```

El modelo local Qwen3 1.7B recibe tres observaciones posteriores a los controles y una paráfrasis identificada del art. 9. No recibe un navegador, herramientas de ejecución ni permiso para aceptar riesgos. Su solicitud, fuentes, digest, salida y errores de validación quedan auditados.

En la interfaz lee la propuesta y abre sus fuentes. Selecciona una afirmación completa, cita un ID que el modelo recibió y explica si realmente la respalda. Una referencia válida puede no respaldar la conclusión. Corrige o rechaza si atribuye cumplimiento, incidente real, recuperación o efectos no observados. Si no hay exceso, justifica la aceptación sin borrar las limitaciones.

El formulario no acepta aprobación de una salida con errores estructurales. Si el modelo está apagado o falla, conserva tu trabajo y vuelve a intentar; no se sustituye una inferencia real por una respuesta precargada.

Exporta el expediente con el botón de la plataforma. Contiene eventos, hashes, análisis, borradores, propuesta de excepción, consulta real y revisión humana. Ningún borrador se envía a ANCI. Entrega al dueño qué decisión queda pendiente de su autoridad.

## Marco de datos y hechos reales

Este dossier fija fecha **21 de octubre de 2026**. Distingue la [Ley 19.628 en su versión aplicable a esa fecha](https://www.bcn.cl/leychile/Navegar?idNorma=141599&idVersion=2023-05-09) de la reforma de [Ley 21.719, cuya entrada en vigencia es el 1 de diciembre de 2026](https://www.bcn.cl/balance-legislativo/detalle/ficha_LEY_21719_2024-12-13). No adelantes automáticamente obligaciones del régimen futuro al caso fechado. En este laboratorio no se procesan datos personales reales.

El caso [Synnovis documentado por NHS England](https://www.england.nhs.uk/synnovis-cyber-incident/questions-and-answers/) permite discutir cómo un proveedor de patología puede afectar capacidad diagnóstica. No se atribuye al caso real la falla de autorización de este rango ni una causa técnica que su fuente no documente. Completa el [cuaderno](CUADERNO.md) y defiende tu expediente ante otro estudiante que actúe como dueño.
