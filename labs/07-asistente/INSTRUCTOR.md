# Audita al asistente · guía docente

Preparar este taller después de explicar sus conceptos y el caso documentado. No hay controles ni entregas calificadas intermedias. La plataforma otorga PX por pruebas y estructura; el juicio profesional se discute.

## Preparación

Usar una instalación individual por estudiante, 16 GB físicos como referencia y Docker con 8 GiB. Preparar imágenes y modelo antes de la sesión. Mantener ZAP apagado en el perfil PHP. Revisar [validación y límites](../../docs/VALIDACION_7_10.md); no declarar un piloto físico aún no realizado.

## El encargo de NubeAndes

Pregunta de apertura: ¿Qué tendrías que ver para aceptar que el portal quedó corregido?

Observación esperada: El contrato identifica una función, un dueño y un límite de prueba. La afirmación del proveedor sigue siendo una hipótesis.

Criterio para discutir: Escribe tu hipótesis sin IA. Separa la versión disponible de la que atiende. Si el servicio deja de entregar documentos, ¿quién puede aceptar ese efecto?

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Dos avisos, condiciones distintas

Pregunta de apertura: ¿Las dos CVE tienen las mismas precondiciones?

Observación esperada: PHP-618 describe OOM; PHP-619, estado global entre solicitudes. Son paráfrasis con enlaces a avisos primarios.

Criterio para discutir: Haz dos filas: condición, SAPI, prueba pertinente y límite. No transfieras una demostración de mod_php a FPM sin evidencia.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La primera propuesta

Pregunta de apertura: ¿Qué afirmación sería peligrosa aunque tenga una cita válida?

Observación esperada: Una inferencia local real, su digest y los fragmentos entregados al modelo. Puede acertar, omitir condiciones o atribuirse pruebas.

Criterio para discutir: Copia una afirmación literal; abre su fuente. Dictamina sobre su contenido, no solo sobre si el ID existe. No uses la respuesta como comprobación de runtime.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Una orden dentro del documento

Pregunta de apertura: ¿Una instrucción dentro de la nota del proveedor debe tener autoridad?

Observación esperada: Otra inferencia real añade DOC-PROVEEDOR. El resultado puede resistir o seguir la instrucción; no se fuerza un fallo para avanzar.

Criterio para discutir: Compara una afirmación de ambas salidas. Incluso si el modelo resiste, explica qué control externo impide que una respuesta cambie el portal.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La comparación vuelve a ti

Pregunta de apertura: ¿La diferencia se debe al documento, al modelo o a lo que no mediste?

Observación esperada: Ambas consultas quedan en el expediente; la comparación no exige que una sea maliciosa ni que la otra sea correcta.

Criterio para discutir: Redacta tu síntesis corregida. Cita consulta, fuente y límite. Una sola pareja de consultas no permite estimar una tasa de éxito de inyección.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## La autoridad fuera del modelo

Pregunta de apertura: ¿Qué ocurriría si el modelo ordenara desplegar ahora?

Observación esperada: La comprobación registra que no se ofrecieron herramientas y que el estado operativo permaneció igual durante las inferencias.

Criterio para discutir: Dibuja fuente → modelo → revisión → acción autorizada → comprobador. Tener un prompt defensivo no sustituye esta separación.

Pide un ID concreto y una objeción que cambiaría la decisión. Si el alumno resuelve rápido el comando, profundiza en alcance, alternativa y defensa; no conviertas la práctica en espera.

## Contraste y cierre

El caso PHP es una divulgación real; el portal, los dueños y los efectos de negocio son ficticios. El perfil implementa versiones mod_php reales y una regresión funcional pequeña. No ejecuta los PoC de las CVE, no abre una webshell ni demuestra RCE. Las condiciones de cada aviso se analizan por separado. La configuración de memoria del contenedor permanece acotada.

En el tramo final se transfiere el método a ArchivoSur y se calculan índices coherentes con el vector elegido. El dueño debe justificar ese vector; la plataforma solo comprueba la aritmética. La OIV es un supuesto docente. Reutilizar las [fuentes jurídicas fechadas](../../docs/FUENTES_4_6.md), distinguiendo vulnerabilidad, incidente y afectación significativa, sin inferir cumplimiento a partir de un mapeo.

La defensa pública es formativa. Prepara fuera del repositorio un expediente distinto para el único examen final: cambia función, alternativa, evidencias y supuestos, manteniendo las habilidades practicadas. Evalúa trazabilidad, proporcionalidad del tratamiento, comprobación posterior y defensa ante una objeción; no velocidad ni memorización de IDs.
