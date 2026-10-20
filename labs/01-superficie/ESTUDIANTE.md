# Terreno · reconstruye antes de decidir

Tu misión es conocer el servicio y las perspectivas de acceso. Abre el laboratorio, entra al puesto por **noVNC** o **SSH** y sigue un objetivo a la vez. Para SSH, pulsa **Conectar por SSH** o ejecuta `./lab.sh ssh` / `.\lab.ps1 ssh` desde tu equipo: usuario `student`, llave de práctica publicada, sin contraseña. Ambos accesos comparten progreso. Consulta [la guía SSH](../../docs/SSH.md). Todo ocurre dentro de la empresa ficticia. Los datos son sintéticos y los puntos no son una nota.

## 1. Primer contacto

Predice con qué identidad trabajarás. En la terminal del puesto (noVNC o SSH) ejecuta:

```bash
lab iniciar
```

Comprueba `uid=1000(student)`, `analisis` y el identificador ST. El tablero acredita el objetivo después de recoger esa evidencia. Escribe en tu cuaderno personal qué diferencia hay entre tu host y el computador remoto.

## 2. El servicio sigue vivo

Predice qué dependencia puede necesitar una transacción. Desde análisis:

```bash
curl -s http://gateway:8080/api/transaction | jq
```

Busca `status: completed` y un identificador TRAIN. Dibuja usuario → gateway → records. Explica por qué una respuesta exitosa todavía no demuestra seguridad.

## 3. El límite de la red

Antes de ejecutar, predice cuáles de los tres servicios podrás alcanzar:

```bash
lab red
```

Compara DNS y TCP. Gateway es accesible; records y backup no se resuelven desde esta zona. Confronta eso con la transacción anterior: un activo puede existir y participar en el negocio sin estar expuesto directamente a tu puesto.

## 4. La puerta inesperada

```bash
curl -s http://gateway:8080/api/export | jq
curl -s http://gateway:8080/api/diagnostics | jq
```

Examina ambos resultados. Separa datos entregados, verificación de identidad y topología publicada. La falla de autorización es original de este laboratorio: no es la CVE de MOVEit. Formula una contraprueba y una pregunta que necesites hacer al dueño.

## 5. Otro punto de vista

Desde análisis entra a soporte:

```bash
ssh ops
lab red
curl -s -H 'X-Training-Key: training-backup-key' http://backup:8082/catalog | jq
```

El prompt ahora corresponde a soporte. Compara su acceso con el de análisis. El catálogo declara permisos; no has borrado datos ni restaurado una copia. Explica por qué «tengo backup» no equivale a «puedo recuperar el servicio». Vuelve con `exit`.

## Defensa del equipo

Construye una matriz puesto/servicio y una cadena de dependencia. Para cada afirmación señala evidencia, perspectiva y límite. Otro equipo elige una afirmación para refutarla. Abre el cuaderno de la plataforma y conserva el expediente; las notas de discusión pueden acompañarlo por separado.

Continúa en [Señales](../02-evidencia/ESTUDIANTE.md).
