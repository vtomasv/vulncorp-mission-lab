# Defiende el expediente · guía del estudiante

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

## 1. Otro dueño, otra decisión

**Antes de actuar:** ¿Cambiar el dueño obliga a repetir todos los comandos o a revisar el alcance?

En **aplicaciones**:

```bash
lab cierre-caso
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/cierre-caso.json` (pulsa `q` para salir).

**Resultado que debes examinar:** ArchivoSur es otro cliente ficticio. Se conservan las comprobaciones actuales del mismo portal, con una función y alternativa distintas.

**Interpreta y contrasta:** Distingue qué observaciones puedes reutilizar y qué impactos exige validar el nuevo dueño. OIV es un supuesto del ejercicio, no una designación real.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 2. La objeción del otro equipo

**Antes de actuar:** ¿Qué prueba podría refutar tu decisión de cierre?

En **aplicaciones**:

```bash
lab cierre-probar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/cierre-probar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Se repiten identidad web, documento y multipart sobre la revisión actual; las respuestas quedan referenciadas.

**Interpreta y contrasta:** Elige una objeción verificable: imagen antigua, hash distinto, función perdida o evidencia anterior al cambio. Explica también lo que este conjunto de pruebas no podría detectar.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 3. Un mapa que permite volver al hecho

**Antes de actuar:** ¿El mismo portal tiene necesariamente el mismo índice con otro dueño?

Este objetivo usa las evidencias ya conservadas; no requiere un comando nuevo. Abre las fuentes desde la misión.

**Resultado que debes examinar:** El formulario comprueba 4 × L × mayor impacto para el vector elegido. La justificación del vector y las asociaciones requieren revisión humana.

**Interpreta y contrasta:** Relaciona riesgo → tratamiento → control → prueba. T1190 sigue siendo una hipótesis de amenaza: no observaste RCE. A.8.8 y A.8.13 orientan gestión y copias; no certifican cumplimiento. Consulta las fuentes jurídicas de la fecha del caso.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 4. La IA revisa el expediente actual

**Antes de actuar:** ¿La IA distingue una observación actual de una afirmación del guion?

En **aplicaciones**:

```bash
lab cierre-ia
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/cierre-ia.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Tercera inferencia real, con avisos y una respuesta actual del documento. Conserva digest, fuentes, límites y revisión.

**Interpreta y contrasta:** Contrasta una afirmación literal con el evento que recibió. Si afirma RCE, cierre integral o aceptación de riesgo, corrígela. El modelo no firma por el dueño.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 5. El expediente sale de la pantalla

**Antes de actuar:** ¿Otro profesional podría reconstruir tu decisión sin ver tu pantalla?

En **aplicaciones**:

```bash
lab cierre-exportar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/cierre-exportar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Un JSON exportado en ~/evidence/cierre-exportar.json y un SHA-256 de su contenido canónico. Incluye eventos, análisis e inferencias conservadas hasta ese instante.

**Interpreta y contrasta:** Une una decisión con un cambio y una prueba posterior. El hash detecta cambios del contenido bajo esa serialización; no autentica al propietario administrador del host.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 6. Defensa ante el dueño

**Antes de actuar:** ¿Qué hecho concreto te obligaría a reabrir mañana?

Este objetivo usa las evidencias ya conservadas; no requiere un comando nuevo. Abre las fuentes desde la misión.

**Resultado que debes examinar:** Tu defensa conserva decisión, objeción, respuesta, responsable y disparador. Los PX siguen siendo formativos.

**Interpreta y contrasta:** Pide a un compañero una objeción sustentada. Tras conservar la defensa, vuelve a exportar para incluir también el análisis final. Este ensayo público no es el examen calificado.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## Si no avanza

- Comprueba que estás en aplicaciones y en el objetivo que habilita la acción. Los cambios posteriores no pueden saltar el análisis anterior.
- Si no responde PHP, ejecuta `php-on` en tu equipo y conserva la campaña. Si no hay inferencia, revisa `ai-on` y los pesos; no sustituyas la respuesta por una captura o un texto inventado.
- Una evidencia de otra campaña, otro episodio o anterior al último cambio no sustituye la prueba actual. Lee la condición pendiente y repite solo la prueba pertinente.
- Si el modelo devuelve una salida defectuosa, conserva el error, revisa la salida completa y vuelve a intentar la consulta. La práctica no exige que el modelo falle ante la nota hostil.

## Extensión de criterio

Intercambia roles de analista, dueño y revisor. El revisor debe proponer una objeción que pueda comprobarse; el dueño explica qué consecuencia tolera y cuál no. Reescribe una conclusión excesiva con su fuente, su alcance y el dato que todavía falta. No agregues solicitudes repetidas para simular más trabajo.

[Cuaderno de evidencia](CUADERNO.md) · [Orientación del instructor](INSTRUCTOR.md) · [Diseño del tramo y límites](../../docs/CONTINUACION_7_10.md)

Después de conservar la defensa, en aplicaciones ejecuta de nuevo `lab cierre-exportar` para incluir los 24 análisis de este tramo. Desde tu equipo puedes conservar el expediente general con `./lab.sh export` (Windows: `.\lab.ps1 export`), que lo guarda en `artifacts/expediente.json`. No publiques tus respuestas como un examen real.
