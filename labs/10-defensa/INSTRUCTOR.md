# Defiende el expediente · guía docente

Preparar este taller después de explicar sus conceptos y el caso documentado. No hay controles ni entregas calificadas intermedias. La plataforma otorga PX por pruebas y estructura; el juicio profesional se discute.

## Preparación

Usar una instalación individual por estudiante, 16 GB físicos como referencia y Docker con 8 GiB. Preparar imágenes y modelo antes de la sesión. Mantener ZAP apagado en el perfil PHP. Revisar [validación y límites](../../docs/VALIDACION_7_10.md); no declarar un piloto físico aún no realizado.

## Otro dueño, otra decisión

Pregunta de apertura: ¿Cambiar el dueño obliga a repetir todos los comandos o a revisar el alcance?

Observación esperada: ArchivoSur es otro cliente ficticio. Se conservan las comprobaciones actuales del mismo portal, con una función y alternativa distintas.

Criterio para discutir: Distingue qué observaciones puedes reutilizar y qué impactos exige validar el nuevo dueño. OIV es un supuesto del ejercicio, no una designación real.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La objeción del otro equipo

Pregunta de apertura: ¿Qué prueba podría refutar tu decisión de cierre?

Observación esperada: Se repiten identidad web, documento y multipart sobre la revisión actual; las respuestas quedan referenciadas.

Criterio para discutir: Elige una objeción verificable: imagen antigua, hash distinto, función perdida o evidencia anterior al cambio. Explica también lo que este conjunto de pruebas no podría detectar.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Un mapa que permite volver al hecho

Pregunta de apertura: ¿El mismo portal tiene necesariamente el mismo índice con otro dueño?

Observación esperada: El formulario comprueba 4 × L × mayor impacto para el vector elegido. La justificación del vector y las asociaciones requieren revisión humana.

Criterio para discutir: Relaciona riesgo → tratamiento → control → prueba. T1190 sigue siendo una hipótesis de amenaza: no observaste RCE. A.8.8 y A.8.13 orientan gestión y copias; no certifican cumplimiento. Consulta las fuentes jurídicas de la fecha del caso.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La IA revisa el expediente actual

Pregunta de apertura: ¿La IA distingue una observación actual de una afirmación del guion?

Observación esperada: Tercera inferencia real, con avisos y una respuesta actual del documento. Conserva digest, fuentes, límites y revisión.

Criterio para discutir: Contrasta una afirmación literal con el evento que recibió. Si afirma RCE, cierre integral o aceptación de riesgo, corrígela. El modelo no firma por el dueño.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## El expediente sale de la pantalla

Pregunta de apertura: ¿Otro profesional podría reconstruir tu decisión sin ver tu pantalla?

Observación esperada: Un JSON exportado en ~/evidence/cierre-exportar.json y un SHA-256 de su contenido canónico. Incluye eventos, análisis e inferencias conservadas hasta ese instante.

Criterio para discutir: Une una decisión con un cambio y una prueba posterior. El hash detecta cambios del contenido bajo esa serialización; no autentica al propietario administrador del host.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Defensa ante el dueño

Pregunta de apertura: ¿Qué hecho concreto te obligaría a reabrir mañana?

Observación esperada: Tu defensa conserva decisión, objeción, respuesta, responsable y disparador. Los PX siguen siendo formativos.

Criterio para discutir: Pide a un compañero una objeción sustentada. Tras conservar la defensa, vuelve a exportar para incluir también el análisis final. Este ensayo público no es el examen calificado.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Contraste y cierre

El caso PHP es una divulgación real; el portal, los dueños y los efectos de negocio son ficticios. El perfil implementa versiones mod_php reales y una regresión funcional pequeña. No ejecuta los PoC de las CVE, no abre una webshell ni demuestra RCE. Las condiciones de cada aviso se analizan por separado. La configuración de memoria del contenedor permanece acotada.

En el tramo final se transfiere el método a ArchivoSur y se calculan índices coherentes con el vector elegido. El dueño debe justificar ese vector; la plataforma solo comprueba la aritmética. La OIV es un supuesto docente. Reutilizar las [fuentes jurídicas fechadas](../../docs/FUENTES_4_6.md), distinguiendo vulnerabilidad, incidente y afectación significativa, sin inferir cumplimiento a partir de un mapeo.

La defensa pública es formativa. Prepara fuera del repositorio un expediente distinto para el único examen final: cambia función, alternativa, evidencias y supuestos, manteniendo las habilidades practicadas. Evalúa trazabilidad, proporcionalidad del tratamiento, comprobación posterior y defensa ante una objeción; no velocidad ni memorización de IDs.
