# IA local en CPU

## Perfil de referencia

Ollama fijado por digest en Compose. Modelo **Qwen3 1.7B**, un modelo cargado, una inferencia por vez, dos CPU y límite de 4 GiB. La consulta usa `num_gpu: 0`, contexto de 4096, salida estructurada, temperatura 0 y hasta 650 tokens de generación. No se promete determinismo exacto ni un tiempo fijo.

Preparación en una terminal dentro del repositorio:

```bash
./lab.sh ai-prepare
./lab.sh ai-on
```

Windows: `.\lab.ps1 ai-prepare`, `.\lab.ps1 ai-on`. Antes debe haberse ejecutado `up` para construir la imagen del centro de misión.

`ai-prepare` descarga el motor y pesos mediante una red temporal, luego recrea Ollama desde el Compose base para retirarla, incluso si falla la descarga. Si interrumpiste el proceso de forma forzada, ejecuta el modo normal `docker compose --profile ai up -d --force-recreate ollama` para comprobar que se retiró la red temporal antes de continuar. No se configura un proveedor cloud ni se publica el puerto 11434.

`ai-on` mantiene puestos y servicios activos. `ai-off` detiene únicamente Ollama y libera su memoria; no reinicia targets ni elimina medidas. El presupuesto combinado del juego con IA es 6752 MiB en límites de contenedor; usa Docker con 8 GiB y una herramienta pesada a la vez.

## Qué hace la consulta

1. En el objetivo «Una segunda mirada», el estudiante ejecuta `lab ia` desde aplicaciones. Esta consulta guiada usa salud y F-02; la API admite uno o dos hallazgos como extensión.
2. Recuperación local simple: IDs relacionados y coincidencia léxica, máximo cuatro fragmentos.
3. El modelo recibe la pregunta, parte del dossier y evidencia rotulada como no confiable.
4. Devuelve resumen, hechos candidatos con IDs, preguntas, opciones y límites.
5. El validador comprueba estructura y que los IDs existan en **los fragmentos recibidos**.
6. Se registra la inferencia y se pide revisión humana.

Es un flujo RAG pequeño y visible, no una búsqueda exhaustiva ni un sistema de inteligencia actualizado en tiempo real. Una referencia existente puede estar mal usada. El modelo no ve logs nuevos por sí mismo, no ha ejecutado pruebas y no recibe la autoridad para aprobar una decisión.

## Lo que queda fuera de su autoridad

No hay tools, shell, Docker socket, credenciales reales ni endpoints de cambio concedidos al modelo. La respuesta solo se presenta como texto escapado. Los cambios se solicitan desde el puesto mediante una acción separada, y riesgo/SSVC se calculan mediante código determinista. El control principal es capacidad y permisos, no confiar en que un prompt detendrá todas las instrucciones adversarias.

## Auditoría

El expediente conserva pregunta, solicitud exacta (mensajes, esquema y parámetros), modelo y digest observado por `/api/tags`, versión y hash del prompt construido, IDs/textos recuperados, salida, validación, tiempo y revisión humana. El hash no contiene una prueba criptográfica de autoría ni asegura corrección de contenido.

El modelo de referencia debe coincidir con `data/model-lock.json`; si el tag remoto cambia de contenido, la aplicación bloquea su uso hasta revisar la procedencia y actualizar explícitamente el lock. El digest identifica contenido, no es una firma del publicador. Un modelo alternativo seleccionado explícitamente se registra sin verificación del digest y exige validación propia.

Para medir valor registra tiempo de análisis **más tiempo de revisión**, afirmaciones sustentadas, omisiones peligrosas y necesidad de contexto. Una respuesta más extensa o un modelo más grande no implica mejor decisión.

## Si la inferencia falla

El terminal muestra el error y el objetivo espera una consulta real. La aplicación no inventa una respuesta para aparentar IA. El objetivo permanece pendiente si no hubo inferencia real. La captura histórica de docs/ejemplos sirve para discusión, no concede puntos. Conserva tu decisión manual y repite la consulta cuando el motor esté disponible.

Consulta de estado:

```bash
docker compose --profile ai ps
docker compose logs --tail=50 ollama
docker compose exec ollama ollama list
```

## Extensión opcional: 4B

Solo después de medir 1.7B y sin cargar ambos modelos a la vez. Usa una **variable de sesión** coherente para que lanzador y Compose seleccionen el mismo modelo:

```bash
export OLLAMA_MODEL=qwen3:4b
./lab.sh ai-prepare
./lab.sh ai-on
```

PowerShell: `$env:OLLAMA_MODEL='qwen3:4b'`. No es un requisito para la clase ni se considera validado hasta medir consumo y calidad. Para volver, elimina la variable y repite `ai-on` con la configuración de referencia.

## Revisión del expediente OIV

En el último objetivo de Gobierno, `lab ia-expediente` ejecuta una inferencia real con tres pruebas posteriores a autorización y revocación y una paráfrasis identificada del art. 9 de la Ley 21.663. Se conserva el contenido exacto recibido por el modelo. El borrador se identifica con `purpose: oiv-dossier`, episodio y campaña. La revisión humana queda en `lab_record`, con audit ID, dictamen, fundamento y entrega pendiente al dueño. Debe citar un ID realmente recibido. Una salida estructuralmente inválida se puede corregir o rechazar, pero no aceptar.

El modelo no calcula vencimientos jurídicos, no ejecuta controles ni acepta excepciones. Los vencimientos se calculan de forma determinista sobre el dossier fechado. El tratamiento de evidencia no confiable y las restricciones de ejecución del asistente se mantienen. `webscan-off` puede liberar memoria antes de esta inferencia CPU.

## Comparación y revisión en el tramo final

Los objetivos nuevos ejecutan tres inferencias locales: avisos resumidos, avisos más una nota ficticia con instrucciones incrustadas y revisión con un evento actual del documento. Se conservan solicitud, fuentes, digest, salida, errores de esquema y dictamen humano. La comparación no exige que el modelo obedezca la nota hostil. El controlador verifica que no ofreció herramientas y que el estado operativo no cambió durante cada inferencia.

La memoria configurada con ambos PHP e IA suma 7360 MiB; ZAP se detiene al activar PHP. [Guía de IA y fuentes](../labs/07-asistente/ESTUDIANTE.md).
