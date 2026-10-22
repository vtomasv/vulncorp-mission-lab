# Cambia el servicio real · PHP2Shell · guía docente

Preparar este taller después de explicar sus conceptos y el caso documentado. No hay controles ni entregas calificadas intermedias. La plataforma otorga PX por pruebas y estructura; el juicio profesional se discute.

## Preparación

Usar una instalación individual por estudiante, 16 GB físicos como referencia y Docker con 8 GiB. Preparar imágenes y modelo antes de la sesión. Mantener ZAP apagado en el perfil PHP. Revisar [validación y límites](../../docs/VALIDACION_7_10.md); no declarar un piloto físico aún no realizado.

## El PHP que atiende tráfico

Pregunta de apertura: ¿Por qué php -v puede decir 8.4.27 y el portal seguir en 8.4.26?

Observación esperada: CLI real del contenedor candidato y respuesta HTTP real del despliegue activo. Web: versión 80426, SAPI apache2handler; CLI candidato: 8.4.27.

Criterio para discutir: Compara deployment y base_digest. Son dos despliegues identificados, no dos versiones inventadas en la misma instalación. Explica por qué no puedes cerrar todavía.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La línea base del servicio

Pregunta de apertura: ¿Qué sería perder la función del cliente?

Observación esperada: Documento NUBE-001 con status completed y hash, identidad del proceso web y una petición multipart pequeña aceptada.

Criterio para discutir: Anota antes de cambiar: versión, SAPI, despliegue, revisión, HTTP, hash y accepted. HTTP 200 no acredita RCE ni ausencia de vulnerabilidades.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La medida parcial

Pregunta de apertura: ¿Bloquear un formato actualiza PHP?

Observación esperada: La frontera devuelve 415 para la sonda multipart; el portal sigue entregando el documento y el runtime conserva 8.4.26.

Criterio para discutir: La restricción se aplica en el controlador de esta ruta, antes de PHP. No es un parche ni una mitigación completa de ambas CVE; no cubre otros consumidores o rutas.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## El dueño autoriza un cambio

Pregunta de apertura: ¿Qué resultado obligaría al dueño a detener o revertir el cambio?

Observación esperada: Tu plan conserva autoridad, criterios verificables y condición de reversión antes de activar el candidato.

Criterio para discutir: Define tres pruebas: versión web corregida, documento legítimo, multipart funcional. Revertir hacia la imagen antigua reintroduce el riesgo y exige una decisión explícita.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## El candidato recibe tráfico

Pregunta de apertura: ¿Qué tiene que cambiar en una respuesta que antes servía el runtime antiguo?

Observación esperada: La ruta del controlador pasa al contenedor corregido real; versión 80427 y digest fijado. La restricción de formato se retira.

Criterio para discutir: Compara el antes y el después. No se recompila PHP en este paso ni se eliminan todos los procesos antiguos: se cambia entre dos despliegues precargados y aislados.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Un cierre que admite límites

Pregunta de apertura: ¿Un control negativo aislado basta para cerrar?

Observación esperada: PHP corregido, documento completado y multipart funcional aceptado después del cambio, con la revisión actual.

Criterio para discutir: Explica la diferencia entre regresión funcional y reproducción de una CVE. Este perfil no contiene PoC RCE ni demuestra que desaparecieron todas las vulnerabilidades.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Contraste y cierre

El caso PHP es una divulgación real; el portal, los dueños y los efectos de negocio son ficticios. El perfil implementa versiones mod_php reales y una regresión funcional pequeña. No ejecuta los PoC de las CVE, no abre una webshell ni demuestra RCE. Las condiciones de cada aviso se analizan por separado. La configuración de memoria del contenedor permanece acotada.

En el tramo final se transfiere el método a ArchivoSur y se calculan índices coherentes con el vector elegido. El dueño debe justificar ese vector; la plataforma solo comprueba la aritmética. La OIV es un supuesto docente. Reutilizar las [fuentes jurídicas fechadas](../../docs/FUENTES_4_6.md), distinguiendo vulnerabilidad, incidente y afectación significativa, sin inferir cumplimiento a partir de un mapeo.

La defensa pública es formativa. Prepara fuera del repositorio un expediente distinto para el único examen final: cambia función, alternativa, evidencias y supuestos, manteniendo las habilidades practicadas. Evalúa trazabilidad, proporcionalidad del tratamiento, comprobación posterior y defensa ante una objeción; no velocidad ni memorización de IDs.
