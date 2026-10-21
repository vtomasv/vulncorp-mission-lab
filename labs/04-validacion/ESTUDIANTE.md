# Comprueba la ruta

Tu misión es entregar un dictamen que otra persona pueda reproducir. Primero defines qué está permitido; después diferencias conexión, ejecución, autenticación y autorización. Trabajarás con `curl`, `jq`, un colector HTTP y OWASP ZAP reales dentro de Docker.

## Antes de entrar

Continúa tu campaña después de **Proteger sin interrumpir**. No se reinician los quince objetivos anteriores. El docente debe actualizar el repositorio, ejecutar `./lab.sh up` y preparar `./lab.sh webscan-on`. En Windows: `.\lab.ps1 up` y `.\lab.ps1 webscan-on`. No necesitas instalar ZAP ni Python en tu equipo.

Abre <http://localhost:8095>. Puedes elegir el escritorio noVNC o entrar desde tu terminal:

```bash
./lab.sh ssh
```

Ya dentro del puesto de análisis:

```bash
ssh appdesk
whoami
hostname
```

Debes ser `student` en aplicaciones. Si estabas en soporte, escribe `exit` antes del salto. **Tu terminal del equipo no está dentro de Docker:** los nombres `gateway`, `validation` y `collector` se usan desde las estaciones, no desde tu sistema anfitrión.

## 1. Un permiso para probar

Antes de ejecutar, redacta una predicción: «si aparece X, podré sostener Y; todavía no podré sostener Z». Acuerda un criterio de detención y un responsable de avisar. Ejemplo de condición observable: respuestas 503 consecutivas o pérdida de la transacción legítima; detener, conservar registro y avisar al responsable del servicio ficticio.

```bash
lab abrir
```

El comando vincula el rango a tu campaña y muestra su `episode`. Repetirlo en la misma campaña conserva los controles. No concede permiso sobre otras empresas o destinos. En la interfaz elige alcance interno y tráfico acotado, y conserva tu fundamento.

El rango agrega dos hallazgos: **R-01**, autorización entre clientes, y **R-02**, uso de una identidad que el guion declara comprometida. Son distintos de **F-02**, la exportación anterior: corregir `/range/live` no corrige `/api/export`.

## 2. Una señal desde dentro

Predice si una conexión saliente basta para demostrar ejecución. Después ejecuta:

```bash
lab callback
```

Busca `request`, `callback`, `collector`, `correlation` y `parent`. La solicitud entra a la aplicación, que llama al colector interno en otro contenedor. Consulta en la interfaz **evidencia del rango** y encuentra ambos registros con la misma correlación.

En el formulario vincula el recibo del colector y explica qué demuestra. Un recibo acredita la conexión que llegó al colector; no acredita por sí solo ejecución de un comando, persistencia, robo de datos ni explotación de una CVE.

## 3. La diferencia está en la prueba

```bash
lab marcador
```

Ahora existe además un evento `marker`, salida `TRAINING-MARKER-ONLY`, código de salida y hash. Relaciona el marcador con la solicitud mediante `parent`, y con el recibo mediante `correlation`.

Este banco ejecuta un subproceso fijo para enseñar la diferencia de evidencia. **No incorpora Log4j, no reproduce Log4Shell y no acepta comandos ni URLs del alumno.** Compara las dos pruebas y explica por qué no corresponde declarar «CVE-2021-44228 explotada».

Investiga el caso real en [CISA, guía Log4Shell](https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a). Distingue el inventario de componentes, la búsqueda de indicios y la respuesta ante compromiso. El paralelo docente es la disciplina de validación, no una réplica del exploit.

## 4. Tu identidad, los datos de otro

Escribe primero la matriz que esperas obtener: identidad × propietario del documento × versión de autorización.

```bash
lab transferencia
```

La línea base compara cuatro solicitudes:

| Ruta | Identidad | Respuesta que debes contrastar |
|---|---|---|
| `/range/vuln/documents/SALUD-001` | Agua | 200: acceso indebido entre clientes |
| `/range/fixed/documents/SALUD-001` | Agua | 403: identidad válida, objeto no autorizado |
| `/range/fixed/documents/SALUD-001` | Salud | 200: función legítima |
| `/range/fixed/documents/SALUD-001` | Sin identidad | 401: falta autenticación |

Reproduce una fila manualmente; el contenido es ficticio:

```bash
curl -sS -i -H 'Authorization: Bearer training-agua-user' \
  http://gateway:8080/range/vuln/documents/SALUD-001
```

Cambia solo `vuln` por `fixed`. Después cambia la identidad por `training-salud-user`. Conserva la diferencia entre 401 y 403; **un 200 no demuestra autorización correcta sin conocer al dueño del objeto**.

Amplía la investigación: prueba el documento `AGUA-001` con ambas identidades, conserva el control positivo de Agua→Agua y el negativo Salud→Agua. Cambia una variable a la vez. Son solicitudes al mismo rango autorizado; no uses un escáner contra destinos externos.

Las credenciales `training-agua-user`, `training-salud-user` y `training-stolen-salud` son públicas, sintéticas y limitadas al rango. Esta última se presenta como comprometida por el guion; no se ha ejecutado su robo.

## 5. El escáner no conoce al dueño

```bash
lab zap
jq '{version, mode, alerts: [.alerts[] | {name,risk,url}]}' ~/evidence/zap-report.json
```

El agente envía cuatro solicitudes fijas a ZAP y espera el análisis pasivo. No usa spider ni escaneo activo. El archivo contiene respuestas, alertas reales, versión, identificador de ejecución y alcance; el recibo firmado conserva su hash. **No hay un número prefijado de alertas que debas obtener.**

Elige una alerta real, explica su efecto y compárala con R-01. Si no hay alertas, documenta cero y el alcance pasivo. ¿El escáner conoce que Agua no es dueño de `SALUD-001`? ¿Puede una alerta de encabezados desplazar una lectura entre clientes que ya reprodujiste? Evita confundir cantidad de alertas con importancia para el negocio.

Si aparece «ZAP no está listo», el docente ejecuta `webscan-on` desde la carpeta del repositorio en el equipo, no dentro de `appdesk`. Conserva tus archivos y repite `lab zap`. Al terminar se puede ejecutar `webscan-off` para liberar memoria.

## 6. Lo que puedes sostener

El dictamen debe incluir:

1. Alcance autorizado y perspectiva de la estación.
2. R-01 con identidad, objeto, versión y respuesta reproducible.
3. Prueba legítima que evita confundir bloqueo con protección útil.
4. Qué demostraron callback y marcador, con sus límites.
5. Qué aportó ZAP y qué dejó sin resolver.
6. Tratamiento recomendado, responsable, criterio de aceptación y dato pendiente del dueño.

Selecciona al menos dos eventos del episodio y conserva tu análisis en la interfaz. Los PX se conceden cuando hay pruebas auténticas y relaciones válidas; no califican la calidad de tu argumento. Exporta el expediente desde **Cuaderno** cuando quieras conservar una copia.

## Investigación para ir más allá de los comandos guiados

Entrega tu matriz completa para dos clientes y dos documentos. Otro estudiante deberá encontrar una conclusión excesiva en tu dictamen y proponer una contraprueba. Repite esa prueba, conserva su respuesta y corrige la conclusión. Explica qué evidencia te haría cambiar de opinión y cuál no responde a la hipótesis.

Usa el [cuaderno de investigación](CUADERNO.md). La discusión y las contrapruebas forman parte del taller aunque no se traduzcan en más PX.
