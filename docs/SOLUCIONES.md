# Resolver un bloqueo

| Síntoma | Paso útil |
|---|---|
| Docker muestra solo Client | Abre el motor y espera; `doctor` debe mostrar Server. |
| Compose no entiende `!override` | Actualiza a Compose 2.24.4 o superior. |
| No carga localhost:8095 | Usa `status`; revisa que mission esté healthy. Si el puerto está ocupado, define LAB_PORT en `.env` y abre ese puerto. |
| El escritorio queda desconectado | Comprueba workstation, ops y appdesk con `status`. Cierra y vuelve a entrar al puesto. |
| No hay terminal | Dentro del escritorio pulsa Ctrl+Alt+T. |
| Pegar no ejecuta | Es intencional: haz clic en la terminal, revisa la línea y pulsa Enter. Ctrl+U limpia una línea duplicada. |
| `lab` dice que el comando pertenece a otro puesto | Mira el prompt y la ubicación de la guía. `exit` vuelve desde SSH a análisis. |
| `ssh ops` falla | Ejecútalo desde análisis. `up` debe haber terminado y los tres puestos estar healthy. |
| `lab escanear` no puede leer la base | Ejecuta `prepare-game`; actualiza la base y aplica permisos de lectura. No descargues desde el puesto interno. |
| IA no disponible | Ejecuta `ai-prepare` y `ai-on`. Revisa Ollama y el digest del modelo; no se sustituye por una respuesta falsa. |
| No se acreditan puntos | Revisa qué prueba falta en el objetivo. Importan puesto, campaña, resultado y, al final, orden posterior al cambio. |
| El cierre no avanza con HTTP 403 | Falta una transacción con `completed`, restricción vigente o residual con ambas pruebas posteriores. |
| Falta RAM | Mantén una herramienta pesada a la vez, usa Qwen3 1.7B y asigna 8 GB a Docker. `ai-off` libera la IA sin detener servicios o puestos. |

Para diagnóstico docente: `docker compose logs --tail=50 mission workstation ops appdesk`. No compartas volúmenes de secretos ni llaves privadas. Los reportes exportables no contienen sus claves.

`reset-targets` reinicia las fallas del caso sin borrar el historial. Los puntos previos representan hitos pasados; no son un indicador de que el control siga activo después de reiniciar.

Las comprobaciones de desarrollo `tests/integration_game.py` y `tests/ui.mjs` crean una campaña nueva y conservan las anteriores. No las ejecutes durante una partida que quieras continuar como campaña activa.
