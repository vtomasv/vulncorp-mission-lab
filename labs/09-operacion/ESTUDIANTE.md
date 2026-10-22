# Recupera la operación · guía del estudiante

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

## 1. La deriva reabre el cierre

**Antes de actuar:** ¿Una evidencia válida ayer puede ser insuficiente hoy?

En **aplicaciones**:

```bash
lab ops-deriva
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-deriva.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Una reversión de ruta controlada vuelve realmente a PHP 8.4.26. El dueño también cambia el contexto del servicio.

**Interpreta y contrasta:** Reabre el tratamiento. Conserva los resultados históricos como historia, sin usarlos como evidencia del estado actual. Distingue el cambio técnico medido del impacto ficticio.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 2. La alternativa del dueño desaparece

**Antes de actuar:** ¿Qué cambia en la prioridad si desaparece la alternativa manual?

En **aplicaciones**:

```bash
lab ops-contener
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-contener.json` (pulsa `q` para salir).

**Resultado que debes examinar:** La contención vuelve al despliegue corregido. El contexto del incidente propone L=4 e impactos 5/2/5/4; la política ordinal produce 80.

**Interpreta y contrasta:** Calcula 4 × 4 × max(5,2,5,4). Es el escenario que se acaba de priorizar, antes de inferir una reducción de L por la contención. El dueño justifica el vector; 80 no es un porcentaje ni un SLA legal.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 3. Una copia que puedes verificar

**Antes de actuar:** ¿Tener una copia demuestra que sabes restaurar?

En **aplicaciones**:

```bash
lab ops-copiar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-copiar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** El servicio escribe una copia real del documento y comprueba que su hash coincide con el documento observado.

**Interpreta y contrasta:** Conserva el hash de la copia antes de provocar la interrupción. La restauración sigue pendiente: todavía no afirmes recuperación comprobada.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 4. El puerto sigue abierto

**Antes de actuar:** ¿Contenedor sano significa servicio de negocio disponible?

En **aplicaciones**:

```bash
lab ops-danar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-danar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** El documento sintético se cambia de forma controlada y responde HTTP 503. /health sigue respondiendo: PHP permanece activo.

**Interpreta y contrasta:** Describe la función perdida y el punto de observación. No hay ransomware ni datos reales destruidos. No borres volúmenes para intentar resolverlo.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 5. La función vuelve con sus datos

**Antes de actuar:** ¿Cómo probarías que recuperaste el documento correcto?

En **aplicaciones**:

```bash
lab ops-restaurar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-restaurar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** La copia se restaura realmente. Su hash coincide con el conservado; documento completed y multipart funcional vuelven a responder.

**Interpreta y contrasta:** Compara copia anterior, contenido restaurado, runtime y revisión. Un documento recuperado no acredita la recuperación completa de todos los sistemas de una empresa.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 6. Métricas con denominador

**Antes de actuar:** ¿Cinco solicitudes de verificación equivalen a cinco incidentes?

En **aplicaciones**:

```bash
lab ops-metricas
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/ops-metricas.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Un episodio de deriva y una restauración. Se muestra el intervalo entre la observación de fallo y la restauración, sin puntuar velocidad.

**Interpreta y contrasta:** Define numerador, denominador, alcance y huecos. El intervalo medido no es el RTO contractual ni la duración total del incidente.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## Si no avanza

- Comprueba que estás en aplicaciones y en el objetivo que habilita la acción. Los cambios posteriores no pueden saltar el análisis anterior.
- Si no responde PHP, ejecuta `php-on` en tu equipo y conserva la campaña. Si no hay inferencia, revisa `ai-on` y los pesos; no sustituyas la respuesta por una captura o un texto inventado.
- Una evidencia de otra campaña, otro episodio o anterior al último cambio no sustituye la prueba actual. Lee la condición pendiente y repite solo la prueba pertinente.
- Si el modelo devuelve una salida defectuosa, conserva el error, revisa la salida completa y vuelve a intentar la consulta. La práctica no exige que el modelo falle ante la nota hostil.

## Extensión de criterio

Intercambia roles de analista, dueño y revisor. El revisor debe proponer una objeción que pueda comprobarse; el dueño explica qué consecuencia tolera y cuál no. Reescribe una conclusión excesiva con su fuente, su alcance y el dato que todavía falta. No agregues solicitudes repetidas para simular más trabajo.

[Cuaderno de evidencia](CUADERNO.md) · [Orientación del instructor](INSTRUCTOR.md) · [Diseño del tramo y límites](../../docs/CONTINUACION_7_10.md)
