# Clase 1 · Lo que no ves también decide

**Duración:** 7 horas efectivas. **Modalidad:** grupos de 3-4, con reflexión individual. **Evaluación:** formativa, sin nota. [Preparación](../../docs/INICIO.md).

## La llamada de las 08:10

El dueño dice: «Todo funciona. Solo necesito que me digas qué debemos proteger primero». Hay un inventario incompleto, una cuenta de soporte compartida y una API que nadie recuerda haber publicado. Tu misión es reconstruir el servicio antes de hablar de severidades.

Elige **RedSalud Sur**, **Aguas del Valle Sur** o **NubeAndes Servicios** en el aula de práctica. Los nombres, empresas, personas y expedientes son ficticios. La condición OIV es un supuesto académico, no una calificación de una empresa real.

## Al terminar podrás

Relacionar un servicio con sus activos y dueño; comprobar accesibilidad desde dos zonas; distinguir función, exposición y consecuencia; conservar observaciones con límites explícitos.

## Agenda de 420 minutos

| Min | Actividad |
|---:|---|
| 20 | Predecir: qué debería ser público y qué debería ser interno. |
| 40 | Imagen, contenedor, puerto, red, volumen; amenaza, vulnerabilidad y exposición. |
| 30 | Demostración completa: transacción, dependencia, evidencia y límite. |
| 110 | Laboratorio A: iniciar, observar dos zonas y dibujar rutas. |
| 110 | Laboratorio B: encontrar una exposición y entrevistar al dueño. |
| 80 | Comité: tres activos a investigar, cambio de contexto y defensa. |
| 30 | Reflexión individual y exportación. |

Las pausas se programan aparte. Rota cada 20-30 minutos entre **analista**, **operación**, **dueño** y **auditor**. Todas las personas deben ejecutar o explicar una prueba.

## Laboratorio A · Levantar y entender

### Paso 1. Haz una predicción

Antes de ejecutar nada, anota tres frases: «Creo que gateway debe ser accesible desde…», «records depende de…», «si backup falla…». No se corrigen con una nota; las compararás con observaciones.

### Paso 2. Inicia y verifica

```bash
./lab.sh doctor
./lab.sh up
docker compose ps
```

En Windows usa `.\lab.ps1 doctor` y `.\lab.ps1 up`. Debes ver **mission, gateway, records y backup**. Solo el centro de misión publica un puerto en el host, asociado a `127.0.0.1`. Que un servicio no publique un puerto al host no significa que no sea accesible por una ruta de aplicación.

Abre http://localhost:8095. Si no carga, verifica el motor y el puerto; no cambies configuraciones al azar. [Ayuda](../../docs/SOLUCIONES.md).

### Paso 3. Prueba la función del negocio

Pulsa **Probar función de negocio** o ejecuta:

```bash
./lab.sh probe public transaction
```

Salida esperada: `status: 200` y `body.status: completed`, con un ID `TRAIN-...`. El número cambia cada vez. El gateway necesita a records para completar la operación. No se escribe ni se procesa información personal real.

**Pregunta:** si completó una operación, ¿qué puedes afirmar y qué no puedes afirmar sobre seguridad?

### Paso 4. Mira desde la zona pública

```bash
./lab.sh discover public
```

La sonda solo acepta los tres nombres del caso. Debes observar:

- `gateway:8080`: `reachable`.
- `records:8081` y `backup:8082`: no resueltos en esta zona.

No uses las IP observadas como direcciones fijas: Docker puede cambiarlas. Un error DNS desde una zona no demuestra ausencia del activo.

### Paso 5. Mira desde soporte

```bash
./lab.sh discover support
```

Ahora `backup:8082` debe ser accesible; gateway y records no se resuelven en esta red. Compara con la observación anterior. La sonda excluye el plano de gestión del alcance de targets.

### Paso 6. Construye un inventario pequeño

En una hoja compartida o tu cuaderno registra:

| Activo | Función | Dueño por confirmar | Zonas | Acceso observado | Datos | Servicio dependiente |
|---|---|---|---|---|---|---|
| gateway | | | | | | |
| records | | | | | | |
| backup | | | | | | |

Dibuja flechas solo cuando sepas qué representan. Gateway → records es una dependencia funcional. No dibujes records → backup como flujo de producción: el escenario no lo implementa. Dos redes no convierten un servicio en router.

## Laboratorio B · Descubrir la puerta inesperada

### Paso 7. Comprueba la exportación

```bash
./lab.sh probe public export
./lab.sh probe public diagnostics
```

Windows: `.\lab.ps1 probe public export` y `.\lab.ps1 probe public diagnostics`.

Inicialmente export devuelve HTTP 200 y dos expedientes sintéticos sin comprobar autenticación. Diagnostics muestra topología y versiones. **Un SBOM no descubre por sí solo esta falla de autorización.**

Repite las dos pruebas con los botones del mapa para guardarlas en la bitácora. Anota sus IDs de evidencia. Las salidas CLI son observaciones independientes; si quieres incluirlas en la entrega, consérvalas junto al expediente.

**No concluyas** que obtuviste una consola, que accediste a todas las redes o que hubo compromiso de una organización real. Describe exactamente la respuesta y el origen de tu prueba.

### Paso 8. Pregunta al dueño

Abre **Clases y actividades** y las tarjetas del dueño. Antes de leerlas, la persona que representa al dueño debe recibir estas preguntas:

1. ¿Qué función no puede dejar de operar?
2. ¿Qué alternativa manual existe y con qué capacidad?
3. ¿Qué se pierde si no hay recuperación?
4. ¿Quién autoriza un cambio y con qué tolerancia de interrupción?

Registra una dependencia que no podías obtener de un escáner. La criticidad se argumenta con consecuencias y contexto, no se adivina a partir del nombre del servidor.

### Paso 9. Recibe el giro

Vuelve al mapa y pulsa **Revelar nueva información**. El sistema guarda un nuevo hecho sintético de negocio. No modifica los hallazgos técnicos ni borra decisiones previas. Cambia una premisa, no el pasado.

### Paso 10. Defiende tres investigaciones

En comité, elige qué tres cosas investigarías en las próximas horas. Para cada una: activo, exposición comprobada, función dependiente, consecuencia y dato faltante. El auditor debe impugnar una afirmación que vaya más allá de la evidencia.

## Reflexión y salida

Completa las cuatro reflexiones de **Clases y actividades → Clase 1**. Cada explicación debe contener «observé», «esto permite concluir» y «falta comprobar». Exporta tu expediente.

**Éxito observable:** puedes reproducir una ruta desde una zona; distinguir no accesible directamente de accesible por gateway; relacionar el activo con un servicio y un dueño; citar al menos dos observaciones reales.

## Ayudas sin quitarte la decisión

1. **Pista conceptual:** distingue la ruta de red de la ruta HTTP que implementa gateway.
2. **Pista técnica:** compara `discover` con `probe export`. Son preguntas diferentes.
3. **Recuperación:** si el target está apagado, vuelve con `./lab.sh ai-off`; si necesitas el estado inicial, `./lab.sh reset-targets`. La evidencia anterior se conserva y debe leerse con su hora.

**Extensión:** dibuja una hipótesis falsa de movimiento lateral y diseña una prueba que podría refutarla. No añadas herramientas nuevas por el solo hecho de tener tiempo.
