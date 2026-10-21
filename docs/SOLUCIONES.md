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
| `./lab.sh ssh` no conecta | Comprueba que `up` terminó y el puerto local esté libre. `LAB_SSH_PORT` permite elegir otro puerto; vuelve a ejecutar `up`. |
| OpenSSH rechaza los permisos de la llave | Usa el lanzador `ssh`, que prepara una copia con permisos limitados. En macOS/Linux, la conexión manual requiere `chmod 600` al archivo. |
| SSH pide una contraseña | Usuario `student`; se necesita la llave privada de entrenamiento. La autenticación por contraseña está deshabilitada. Usa el lanzador o revisa la ruta después de `-i`. |
| La huella del servidor cambió | Comprueba la huella en la interfaz. El lanzador obtiene la pública de tu contenedor; no desactives la verificación de host. |
| `ssh ops` falla | Ejecútalo desde análisis. `up` debe haber terminado y los tres puestos estar healthy. |
| `lab escanear` no puede leer la base | Ejecuta `prepare-game`; actualiza la base y aplica permisos de lectura. No descargues desde el puesto interno. |
| IA no disponible | Ejecuta `ai-prepare` y `ai-on`. Revisa Ollama y el digest del modelo; no se sustituye por una respuesta falsa. |
| No se acreditan puntos | Revisa qué prueba falta en el objetivo. Importan puesto, campaña, resultado y, al final, orden posterior al cambio. |
| El cierre no avanza con HTTP 403 | Falta una transacción con `completed`, restricción vigente o residual con ambas pruebas posteriores. |
| Falta RAM | Mantén una herramienta pesada a la vez, usa Qwen3 1.7B y asigna 8 GB a Docker. `ai-off` libera la IA sin detener servicios o puestos. |

Para diagnóstico docente: `docker compose logs --tail=50 mission workstation ops appdesk`. El par de entrenamiento de `training/ssh` es intencionalmente público. No compartas volúmenes de secretos, privadas de servidor ni la privada interna entre puestos. Los reportes exportables no contienen sus claves.

`reset-targets` reinicia las fallas del caso sin borrar el historial. Los puntos previos representan hitos pasados; no son un indicador de que el control siga activo después de reiniciar.

Las comprobaciones de desarrollo `tests/integration_game.py` y `tests/ui.mjs` crean una campaña nueva y conservan las anteriores. No las ejecutes durante una partida que quieras continuar como campaña activa.

## Nuevos desafíos de Validación, Trazabilidad y Gobierno

- `lab abrir: comando de otro puesto`: estás en análisis o soporte. Vuelve a análisis con `exit` si corresponde y entra con `ssh appdesk`.
- `ZAP no está listo`: desde la carpeta del repositorio en el equipo ejecuta `./lab.sh webscan-on` o `.\lab.ps1 webscan-on`. Espera a que esté saludable; repite `lab zap` en aplicaciones. La primera descarga requiere Internet.
- El control pide ensayo previo: ejecuta `lab ensayar` antes de `lab corregir`; después repítelo. Para revocar, conserva primero el ensayo con autorización corregida y la llave comprometida todavía aceptada.
- Una técnica no tiene evidencia: usa los eventos del último `lab simular`, no los de otra campaña ni una CVE. Copia el ID preciso y selecciónalo también como fuente.
- La cronología no coincide: `lab cronologia` toma el último conjunto SIM; si vuelves a simular, vuelve a generar el archivo y a ordenar esos tres IDs.
- El cálculo de reportes falla: usa la hora fija del dossier e indica zona horaria. La actualización especial exige OIV y servicio esencial afectado; el final parte del envío de alerta temprana.
- La matriz pide una fuente: abre el expediente original y cita un ID EV existente o una prueba de estación propia en cada fila; explica su límite. Un ID que existe no certifica el argumento.
- La revisión IA no se acepta: ejecuta `lab ia-expediente` en su objetivo, abre sus fuentes y cita una de ellas en tu fundamento. Si hay errores estructurales, corrige o rechaza.

No borres volúmenes para corregir una selección. Los nuevos controles y registros sobreviven a recreación de contenedores en `range_state`; los targets originales mantienen su comportamiento previo de estado en memoria.

El directorio de trabajo de ZAP usa `zap_work` en disco; no se limita a una pequeña carpeta RAM. Si aparece un error de espacio, verificar el disco asignado a Docker y conservar el diagnóstico. No borrar el volumen de evidencia para solucionarlo.
