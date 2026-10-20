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

`ai-on` pausa gateway, records y backup para contener el consumo. La evidencia anterior sigue disponible en SQLite. **Volver con `ai-off` reinicia targets en estado inicial**: una mitigación pasada necesita repetición y nueva prueba.

## Qué hace la consulta

1. El estudiante selecciona cliente y uno o dos hallazgos.
2. Recuperación local simple: IDs relacionados y coincidencia léxica, máximo cuatro fragmentos.
3. El modelo recibe la pregunta, parte del dossier y evidencia rotulada como no confiable.
4. Devuelve resumen, hechos candidatos con IDs, preguntas, opciones y límites.
5. El validador comprueba estructura y que los IDs existan en **los fragmentos recibidos**.
6. Se registra la inferencia y se pide revisión humana.

Es un flujo RAG pequeño y visible, no una búsqueda exhaustiva ni un sistema de inteligencia actualizado en tiempo real. Una referencia existente puede estar mal usada. El modelo no ve logs nuevos por sí mismo, no ha ejecutado pruebas y no recibe la autoridad para aprobar una decisión.

## Lo que queda fuera de su autoridad

No hay tools, shell, Docker socket, credenciales reales ni endpoints de cambio concedidos al modelo. La respuesta solo se presenta como texto escapado. Los cambios se solicitan por un formulario distinto, y riesgo/SSVC se calculan mediante código determinista. El control principal es capacidad y permisos, no confiar en que un prompt detendrá todas las instrucciones adversarias.

## Auditoría

El expediente conserva pregunta, solicitud exacta (mensajes, esquema y parámetros), modelo y digest observado por `/api/tags`, versión y hash del prompt construido, IDs/textos recuperados, salida, validación, tiempo y revisión humana. El hash no contiene una prueba criptográfica de autoría ni asegura corrección de contenido.

El modelo de referencia debe coincidir con `data/model-lock.json`; si el tag remoto cambia de contenido, la aplicación bloquea su uso hasta revisar la procedencia y actualizar explícitamente el lock. El digest identifica contenido, no es una firma del publicador. Un modelo alternativo seleccionado explícitamente se registra sin verificación del digest y exige validación propia.

Para medir valor registra tiempo de análisis **más tiempo de revisión**, afirmaciones sustentadas, omisiones peligrosas y necesidad de contexto. Una respuesta más extensa o un modelo más grande no implica mejor decisión.

## Si la inferencia falla

El panel muestra apagado/sin modelo o error de inferencia. La aplicación no inventa una respuesta para aparentar IA. Hay un ejemplo sintético explícito para discutir errores, que no se registra como inferencia real. Conserva tu decisión manual y repite la consulta cuando el motor esté disponible.

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
