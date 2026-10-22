# Cambia el servicio real · PHP2Shell · guía del estudiante

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

## 1. El PHP que atiende tráfico

**Antes de actuar:** ¿Por qué php -v puede decir 8.4.27 y el portal seguir en 8.4.26?

En **aplicaciones**:

```bash
lab php-inventariar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-inventariar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** CLI real del contenedor candidato y respuesta HTTP real del despliegue activo. Web: versión 80426, SAPI apache2handler; CLI candidato: 8.4.27.

**Interpreta y contrasta:** Compara deployment y base_digest. Son dos despliegues identificados, no dos versiones inventadas en la misma instalación. Explica por qué no puedes cerrar todavía.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 2. La línea base del servicio

**Antes de actuar:** ¿Qué sería perder la función del cliente?

En **aplicaciones**:

```bash
lab php-ensayar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-ensayar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** Documento NUBE-001 con status completed y hash, identidad del proceso web y una petición multipart pequeña aceptada.

**Interpreta y contrasta:** Anota antes de cambiar: versión, SAPI, despliegue, revisión, HTTP, hash y accepted. HTTP 200 no acredita RCE ni ausencia de vulnerabilidades.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 3. La medida parcial

**Antes de actuar:** ¿Bloquear un formato actualiza PHP?

En **aplicaciones**:

```bash
lab php-mitigar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-mitigar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** La frontera devuelve 415 para la sonda multipart; el portal sigue entregando el documento y el runtime conserva 8.4.26.

**Interpreta y contrasta:** La restricción se aplica en el controlador de esta ruta, antes de PHP. No es un parche ni una mitigación completa de ambas CVE; no cubre otros consumidores o rutas.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 4. El dueño autoriza un cambio

**Antes de actuar:** ¿Qué resultado obligaría al dueño a detener o revertir el cambio?

Este objetivo usa las evidencias ya conservadas; no requiere un comando nuevo. Abre las fuentes desde la misión.

**Resultado que debes examinar:** Tu plan conserva autoridad, criterios verificables y condición de reversión antes de activar el candidato.

**Interpreta y contrasta:** Define tres pruebas: versión web corregida, documento legítimo, multipart funcional. Revertir hacia la imagen antigua reintroduce el riesgo y exige una decisión explícita.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 5. El candidato recibe tráfico

**Antes de actuar:** ¿Qué tiene que cambiar en una respuesta que antes servía el runtime antiguo?

En **aplicaciones**:

```bash
lab php-desplegar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-desplegar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** La ruta del controlador pasa al contenedor corregido real; versión 80427 y digest fijado. La restricción de formato se retira.

**Interpreta y contrasta:** Compara el antes y el después. No se recompila PHP en este paso ni se eliminan todos los procesos antiguos: se cambia entre dos despliegues precargados y aislados.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## 6. Un cierre que admite límites

**Antes de actuar:** ¿Un control negativo aislado basta para cerrar?

En **aplicaciones**:

```bash
lab php-validar
```

Cada comando deja un archivo en `~/evidence/`. Puedes leerlo con `less ~/evidence/php-validar.json` (pulsa `q` para salir).

**Resultado que debes examinar:** PHP corregido, documento completado y multipart funcional aceptado después del cambio, con la revisión actual.

**Interpreta y contrasta:** Explica la diferencia entre regresión funcional y reproducción de una CVE. Este perfil no contiene PoC RCE ni demuestra que desaparecieron todas las vulnerabilidades.

Vuelve a la misión activa. Abre **Consultar evidencia**, localiza los IDs y vincula los que sostienen tu respuesta. Conserva el análisis; la comprobación habilita el siguiente objetivo cuando están las pruebas requeridas.

## Si no avanza

- Comprueba que estás en aplicaciones y en el objetivo que habilita la acción. Los cambios posteriores no pueden saltar el análisis anterior.
- Si no responde PHP, ejecuta `php-on` en tu equipo y conserva la campaña. Si no hay inferencia, revisa `ai-on` y los pesos; no sustituyas la respuesta por una captura o un texto inventado.
- Una evidencia de otra campaña, otro episodio o anterior al último cambio no sustituye la prueba actual. Lee la condición pendiente y repite solo la prueba pertinente.
- Si el modelo devuelve una salida defectuosa, conserva el error, revisa la salida completa y vuelve a intentar la consulta. La práctica no exige que el modelo falle ante la nota hostil.

## Extensión de criterio

Intercambia roles de analista, dueño y revisor. El revisor debe proponer una objeción que pueda comprobarse; el dueño explica qué consecuencia tolera y cuál no. Reescribe una conclusión excesiva con su fuente, su alcance y el dato que todavía falta. No agregues solicitudes repetidas para simular más trabajo.

[Cuaderno de evidencia](CUADERNO.md) · [Orientación del instructor](INSTRUCTOR.md) · [Diseño del tramo y límites](../../docs/CONTINUACION_7_10.md)
