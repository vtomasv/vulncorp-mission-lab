# Audita al asistente · guía del estudiante

## Antes de empezar

Continúa tu campaña después del objetivo anterior; no borres progreso ni crees otra empresa. Los PX son formativos y no existe nota por velocidad. El único examen calificado se prepara por separado.

En **tu equipo**, con Docker abierto y desde la carpeta del repositorio:

```bash
./lab.sh up
./lab.sh php-on
./lab.sh ai-on
```

En Windows usa `.\lab.ps1 up`, `.\lab.ps1 php-on` y `.\lab.ps1 ai-on`. Si no descargaste los pesos, ejecuta `ai-prepare` una vez con Internet. `php-on` detiene ZAP para conservar el presupuesto de memoria; no borra evidencia. Usa un modelo y una inferencia a la vez.

Abre http://localhost:8095. Puedes usar **Entrar al puesto** (noVNC) o, en la terminal de tu equipo, `./lab.sh ssh` / `.\lab.ps1 ssh`. Usuario `student`, llave pública de entrenamiento, sin contraseña. Ambos llegan al mismo puesto y avance. Dentro de **análisis** entra a **aplicaciones**:

```bash
ssh appdesk
whoami
hostname
```

Debe aparecer `student`. Los comandos `lab` de este tramo se ejecutan en **aplicaciones**, no en la terminal del anfitrión. Un `exit` vuelve a análisis; otro cierra SSH. Los destinos PHP no tienen puertos públicos ni acceso directo desde los puestos: el instrumento autorizado envía solicitudes fijas al segmento PHP interno.

En cada objetivo: **predice en el cuaderno → ejecuta → abre la evidencia → interpreta → vincula IDs → conserva el análisis**. La plataforma comprueba condiciones técnicas y relaciones; la discusión evalúa tu criterio. No pegues una frase genérica en todos los fundamentos.

## 1. El encargo de NubeAndes

**Antes de actuar:** ¿Qué tendrías que ver para aceptar que el portal quedó corregido?

En **aplicaciones**:

```bash
lab mision-abrir
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/mision-abrir.json` (pulsa `q` para salir).

**Resultado que debes examinar:** El contrato identifica una función, un dueño y un límite de prueba. La afirmación del proveedor sigue siendo una hipótesis.

**Interpreta y contrasta:** Escribe tu hipótesis sin IA. Separa la versión disponible de la que atiende. Si el servicio deja de entregar documentos, ¿quién puede aceptar ese efecto?

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 2. Dos avisos, condiciones distintas

**Antes de actuar:** ¿Las dos CVE tienen las mismas precondiciones?

En **aplicaciones**:

```bash
lab php-fuentes
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-fuentes.json` (pulsa `q` para salir).

**Resultado que debes examinar:** PHP-618 describe OOM; PHP-619, estado global entre solicitudes. Son paráfrasis con enlaces a avisos primarios.

**Interpreta y contrasta:** Haz dos filas: condición, SAPI, prueba pertinente y límite. No transfieras una demostración de mod_php a FPM sin evidencia.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 3. La primera propuesta

**Antes de actuar:** ¿Qué afirmación sería peligrosa aunque tenga una cita válida?

En **aplicaciones**:

```bash
lab ia-base
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ia-base.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Una inferencia local real, su digest y los fragmentos entregados al modelo. Puede acertar, omitir condiciones o atribuirse pruebas.

**Interpreta y contrasta:** Copia una afirmación literal; abre su fuente. Dictamina sobre su contenido, no solo sobre si el ID existe. No uses la respuesta como comprobación de runtime.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 4. Una orden dentro del documento

**Antes de actuar:** ¿Una instrucción dentro de la nota del proveedor debe tener autoridad?

En **aplicaciones**:

```bash
lab ia-hostil
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ia-hostil.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Otra inferencia real añade DOC-PROVEEDOR. El resultado puede resistir o seguir la instrucción; no se fuerza un fallo para avanzar.

**Interpreta y contrasta:** Compara una afirmación de ambas salidas. Incluso si el modelo resiste, explica qué control externo impide que una respuesta cambie el portal.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 5. La comparación vuelve a ti

**Antes de actuar:** ¿La diferencia se debe al documento, al modelo o a lo que no mediste?

Este objetivo usa las evidencias ya conservadas; no requiere un comando nuevo. Abre las fuentes desde la misión.

**Resultado que debes examinar:** Ambas consultas quedan en el expediente; la comparación no exige que una sea maliciosa ni que la otra sea correcta.

**Interpreta y contrasta:** Redacta tu síntesis corregida. Cita consulta, fuente y límite. Una sola pareja de consultas no permite estimar una tasa de éxito de inyección.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 6. La autoridad fuera del modelo

**Antes de actuar:** ¿Qué ocurriría si el modelo ordenara desplegar ahora?

En **aplicaciones**:

```bash
lab ia-frontera
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ia-frontera.json` (pulsa `q` para salir).

**Resultado que debes examinar:** La comprobación registra que no se ofrecieron herramientas y que el estado operativo permaneció igual durante las inferencias.

**Interpreta y contrasta:** Dibuja fuente → modelo → revisión → acción autorizada → comprobador. Tener un prompt defensivo no sustituye esta separación.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## Si no avanza

- Comprueba que estás en aplicaciones y en el objetivo que habilita la acción. Los cambios posteriores no pueden saltar el análisis anterior.
- Si no responde PHP, ejecuta `php-on` en tu equipo y conserva la campaña. Si no hay inferencia, revisa `ai-on` y los pesos; no sustituyas la respuesta por una captura o un texto inventado.
- Una evidencia de otra campaña, otro episodio o anterior al último cambio no sustituye la prueba actual. Lee la condición pendiente y repite solo la prueba pertinente.
- Si el modelo devuelve una salida defectuosa, conserva el error, revisa la salida completa y vuelve a intentar la consulta. La práctica no exige que el modelo falle ante la nota hostil.

## Extensión de criterio

Intercambia roles de analista, dueño y revisor. El revisor debe proponer una objeción que pueda comprobarse; el dueño explica qué consecuencia tolera y cuál no. Reescribe una conclusión excesiva con su fuente, su alcance y el dato que todavía falta. No agregues solicitudes repetidas para simular más trabajo.

[Cuaderno de evidencia](CUADERNO.md) · [Orientación del instructor](INSTRUCTOR.md) · [Diseño del tramo y límites](../../docs/CONTINUACION_7_10.md)
