# Recupera la operación · guía docente

Preparar este taller después de explicar sus conceptos y el caso documentado. No hay controles ni entregas calificadas intermedias. La plataforma otorga PX por pruebas y estructura; el juicio profesional se discute.

## Preparación

Usar una instalación individual por estudiante, 16 GB físicos como referencia y Docker con 8 GiB. Preparar imágenes y modelo antes de la sesión. Mantener ZAP apagado en el perfil PHP. Revisar [validación y límites](../../docs/VALIDACION_7_10.md); no declarar un piloto físico aún no realizado.

## La deriva reabre el cierre

Pregunta de apertura: ¿Una evidencia válida ayer puede ser insuficiente hoy?

Observación esperada: Una reversión de ruta controlada vuelve realmente a PHP 8.4.26. El dueño también cambia el contexto del servicio.

Criterio para discutir: Reabre el tratamiento. Conserva los resultados históricos como historia, sin usarlos como evidencia del estado actual. Distingue el cambio técnico medido del impacto ficticio.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La alternativa del dueño desaparece

Pregunta de apertura: ¿Qué cambia en la prioridad si desaparece la alternativa manual?

Observación esperada: La contención vuelve al despliegue corregido. El contexto del incidente propone L=4 e impactos 5/2/5/4; la política ordinal produce 80.

Criterio para discutir: Calcula 4 × 4 × max(5,2,5,4). Es el escenario que se acaba de priorizar, antes de inferir una reducción de L por la contención. El dueño justifica el vector; 80 no es un porcentaje ni un SLA legal.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Una copia que puedes verificar

Pregunta de apertura: ¿Tener una copia demuestra que sabes restaurar?

Observación esperada: El servicio escribe una copia real del documento y comprueba que su hash coincide con el documento observado.

Criterio para discutir: Conserva el hash de la copia antes de provocar la interrupción. La restauración sigue pendiente: todavía no afirmes recuperación comprobada.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## El puerto sigue abierto

Pregunta de apertura: ¿Contenedor sano significa servicio de negocio disponible?

Observación esperada: El documento sintético se cambia de forma controlada y responde HTTP 503. /health sigue respondiendo: PHP permanece activo.

Criterio para discutir: Describe la función perdida y el punto de observación. No hay ransomware ni datos reales destruidos. No borres volúmenes para intentar resolverlo.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La función vuelve con sus datos

Pregunta de apertura: ¿Cómo probarías que recuperaste el documento correcto?

Observación esperada: La copia se restaura realmente. Su hash coincide con el conservado; documento completed y multipart funcional vuelven a responder.

Criterio para discutir: Compara copia anterior, contenido restaurado, runtime y revisión. Un documento recuperado no acredita la recuperación completa de todos los sistemas de una empresa.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Métricas con denominador

Pregunta de apertura: ¿Cinco solicitudes de verificación equivalen a cinco incidentes?

Observación esperada: Un episodio de deriva y una restauración. Se muestra el intervalo entre la observación de fallo y la restauración, sin puntuar velocidad.

Criterio para discutir: Define numerador, denominador, alcance y huecos. El intervalo medido no es el RTO contractual ni la duración total del incidente.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Contraste y cierre

El caso PHP es una divulgación real; el portal, los dueños y los efectos de negocio son ficticios. El perfil implementa versiones mod_php reales y una regresión funcional pequeña. No ejecuta los PoC de las CVE, no abre una webshell ni demuestra RCE. Las condiciones de cada aviso se analizan por separado. La configuración de memoria del contenedor permanece acotada.

En el tramo final se transfiere el método a ArchivoSur y se calculan índices coherentes con el vector elegido. El dueño debe justificar ese vector; la plataforma solo comprueba la aritmética. La OIV es un supuesto docente. Reutilizar las [fuentes jurídicas fechadas](../../docs/FUENTES_4_6.md), distinguiendo vulnerabilidad, incidente y afectación significativa, sin inferir cumplimiento a partir de un mapeo.

La defensa pública es formativa. Prepara fuera del repositorio un expediente distinto para el único examen final: cambia función, alternativa, evidencias y supuestos, manteniendo las habilidades practicadas. Evalúa trazabilidad, proporcionalidad del tratamiento, comprobación posterior y defensa ante una objeción; no velocidad ni memorización de IDs.
