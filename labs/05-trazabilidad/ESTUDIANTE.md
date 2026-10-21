# Reconstruye y comprueba

Ya demostraste una falla. Ahora debes reconstruir una secuencia, relacionarla con ATT&CK sin inventar etapas y demostrar el efecto de dos controles complementarios. Trabajarás con eventos reales del rango, `jq`, HTTP y una capa compatible con MITRE Navigator.

## 1. Un incidente declarado

Continúa en aplicaciones (`ssh appdesk` desde análisis). Antes de ejecutar, escribe qué esperas observar y qué información solo proviene del guion:

```bash
lab simular
```

Se envían tres solicitudes con correlaciones que empiezan por `SIM-`: una identidad Agua accede al documento Salud en el gemelo vulnerable; una credencial sintética presentada como comprometida usa su acceso a Salud; una petición anónima es rechazada.

El HTTP y sus logs son reales. **El supuesto de que alguien robó la credencial es ficticio:** no hay robo, malware ni víctima real. No atribuyas actor ni procedencia del compromiso a partir de una solicitud que usa una llave pública del ejercicio.

En la interfaz conserva el alcance de esta afirmación y vincula los eventos pertinentes.

## 2. Tres eventos, una historia

```bash
lab cronologia
jq 'sort_by(.sequence) | .[] | {id,sequence,correlation,identity,status}' ~/evidence/cronologia.json
```

El archivo contiene los tres eventos del último `lab simular`. Copia sus IDs `RNG-…` en orden de secuencia, uno por línea, en el formulario. Si repites la simulación, repite también la cronología: usa el último conjunto completo.

Explica qué añade cada dato:

| Dato | Para qué sirve | Límite |
|---|---|---|
| `sequence` | Orden de recepción en ese proceso del servidor | No ordena universalmente procesos distintos |
| `occurred_at` | Tiempo UTC del evento | Relojes distintos pueden desviarse |
| `correlation` | Relacionar solicitudes y observaciones del ensayo | No es identidad del atacante |
| `identity` | Credencial presentada a la aplicación | No demuestra quién la obtuvo ni cómo |
| `status` | Resultado HTTP | Requiere conocer objeto, identidad y regla del negocio |
| `episode` / `boot_id` | Separar ejecuciones y reinicios | No trasladar evidencia histórica a un nuevo episodio |

Para el callback anterior existen registros de dos servicios: no uses sus secuencias locales como una única cronología global. La relación causal viene de `parent` y `correlation`. Si falta un registro, registra el hueco de visibilidad; no completes la historia con una suposición.

## 3. Mapea lo observado

Lee las descripciones oficiales de [T1190](https://attack.mitre.org/techniques/T1190/) y [T1078](https://attack.mitre.org/techniques/T1078/). En este ejercicio:

1. Relaciona T1190 con el evento `SIM-` donde la identidad Agua aprovecha la falla de la aplicación accesible por gateway y lee Salud.
2. Relaciona T1078 con el evento `SIM-` que usa la credencial presentada como comprometida en el guion.
3. Incluye esos dos IDs entre las fuentes seleccionadas.
4. Explica que son conductas de una simulación declarada, no evidencia de robo real ni de una intrusión externa.
5. Descarta T1486: no observaste cifrado. Tampoco inventes persistencia, movimiento lateral ni exfiltración a Internet.

La táctica describe una finalidad; la técnica, una forma de actuar; el procedimiento, cómo se concreta aquí. No hay relación automática «CVE → todas las técnicas». Una asociación normativa tampoco constituye detección ni prevención efectiva.

## 4. Cierra la frontera del objeto

Antes de modificar, predice las tres respuestas de la ruta `live`:

```bash
lab ensayar
```

Conserva la línea base: Agua→Salud 200 indebido, Salud legítimo 200 e identidad comprometida 200. Solo entonces aplica el control:

```bash
lab corregir
lab ensayar
```

Ahora se esperan Agua→Salud **403**, Salud legítimo **200**, identidad comprometida **200**. La última respuesta es la sorpresa: corregir la relación cliente/objeto no revoca una identidad con permiso sobre su propio cliente.

El comando exige que exista el ensayo anterior y que estés en el objetivo correcto. No marques «todo resuelto»: identifica la ruta residual en el formulario. Usa los eventos fechados posteriores al cambio. El sistema no acepta como continuidad un 200 anterior al control.

Comprueba una fila manualmente:

```bash
curl -sS -i -H 'Authorization: Bearer training-agua-user' \
  http://gateway:8080/range/live/documents/SALUD-001
```

La autorización del objeto se corrige solo en `live`. `vuln` conserva el defecto para el contraste; `fixed` ya verificaba propiedad. Ninguna de estas rutas modifica la exportación F-02 del primer tramo.

## 5. Una identidad todavía sirve

La prueba posterior a autorización es también la línea base anterior a revocación. Antes de ejecutar, explica cómo evitarás bloquear a todos los usuarios:

```bash
lab revocar
lab ensayar
```

Resultado que debes contrastar:

| Identidad | Resultado después de ambos controles | Interpretación |
|---|---|---|
| Agua consulta Salud | 403 | Sigue sin autorización sobre el objeto |
| Salud legítimo | 200 | Función legítima conservada |
| Credencial comprometida del guion | 401 | Esa credencial fue revocada |

Relaciona cada prueba con el control al que responde. ¿Qué conclusión sería errónea si solo conservas el 401? ¿Qué ocurriría si revocaras también al usuario legítimo? Registra una prueba que detectaría esa regresión.

## 6. Una capa que se puede auditar

```bash
lab capa
jq '{name,versions,techniques}' ~/evidence/attack-layer.json
```

La capa incluye exactamente las dos técnicas sustentadas, los IDs de sus pruebas, tu análisis y el episodio. Usa el esquema de capa 4.5 de Navigator. No se finge una base ATT&CK completa: se conservan las versiones consultadas de las dos técnicas. El JSON puede importarse posteriormente en Navigator; no se necesita una web externa para completar el taller.

Verifica que no se coloreó T1486. No interpretes color como cobertura del SOC. Para afirmar detección necesitas una regla que se haya disparado con su evidencia; tener un log solo demuestra registro de actividad.

Conserva la revisión y exporta el expediente. Mantén dos estados diferentes: «conducta observada antes» y «resultado de las pruebas después». Aplicar un control no borra la observación histórica.

## Investigación y defensa

Completa el [cuaderno](CUADERNO.md) con una matriz **conducta → evidencia → control → prueba de eficacia → límite**. Otro estudiante debe intentar demostrar que tu control bloqueó también el negocio o dejó otra ruta abierta. Responde con solicitudes acotadas y resultados, no con una afirmación general de que «está seguro».

Contrasta el caso [MOVEit documentado por CISA/FBI](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/35ecb08). Su mecanismo real fue SQLi y actividad posterior: este rango usa autorización de objetos. La lección compartida es investigar conducta y efectos después de tratar la vulnerabilidad; no se reproduce MOVEit ni se adjudica al rango su cadena de ataque.
