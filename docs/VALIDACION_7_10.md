# Validación del tramo 7–10 · 21 octubre 2026

## Alcance y evidencia de ejecución

Se verificaron **24 objetivos nuevos por SSH real desde el anfitrión**, pasando por análisis y aplicaciones, en una campaña separada. Los primeros 33 premios fueron un **fixture explícito de entrada**: esta ejecución no revalida los laboratorios anteriores ni fabrica su evidencia. La selección previa de campaña se restauró al terminar, conservando todo el historial.

La ejecución completa incluye **tres inferencias locales reales** con Qwen3 1.7B y Ollama, CPU, `num_gpu=0`, dos hilos y digest `8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7`. Las tres consultas terminaron en CPU y sus resultados se conservaron para revisión humana. Sus tiempos son observaciones de desarrollo, no tiempos prometidos para un equipo de 16 GB. En una ejecución completa anterior se detectó una referencia ajena a los fragmentos recibidos; se conservó un dictamen de corrección sin aceptar esa salida como válida. El avance no exige que el modelo obedezca la nota hostil.

El recorrido produjo **49 eventos** y un expediente exportado con **24 análisis humanos de prueba**. Se comprobaron CLI candidato 8.4.27 y web activo 8.4.26, bloqueo parcial 415 con PHP antiguo, cambio al runtime 8.4.27, función preservada y regresión multipart posterior. Después se observó una reversión a 8.4.26, retorno al candidato corregido, copia, documento HTTP 503 y restauración del mismo contenido por hash. La copia sobrevivió al reinicio de ambos contenedores PHP.

La exportación posterior a la defensa incluyó los 24 análisis. Su SHA-256 se recalculó desde el contenido canónico y coincidió con el evento del controlador. La repetición de la comprobación no duplicó PX. Las métricas registraron un episodio de deriva y una restauración, sin confundir solicitudes repetidas con incidentes.

`artifacts/validation-continuation-full.json` conserva el informe local reproducible de esta ejecución; no se publica el historial de cada alumno en Git. La campaña que contiene las comprobaciones se identifica en ese archivo.

## Comprobaciones de frontera

Las **76 pruebas unitarias** pasaron. La suite contiene pruebas específicas de rechazo de cambios fuera del objetivo activo, comandos ajenos al catálogo, referencias inventadas, otro episodio/campaña, evidencia anterior a un cambio, versión o digest incorrectos y restauración con hash diferente. También comprueba aritmética del índice, conteo de deriva y exportación después de completar la campaña. Las respuestas de runtime de las pruebas unitarias son **mocks**, no se presentan como ejecución PHP real.

El contrato Compose comprueba dos PHP internos sin puertos, sin socket Docker, usuario 10001, raíz de solo lectura, capacidades eliminadas, llave exclusiva, bases fijadas por digest y presupuesto PHP con IA de 7360 MiB. La integración real comprueba que los puestos no resuelven los dos destinos PHP directamente y que el navegador no obtiene la autoridad de cambio operativo.

La prueba de renderizado recorre los 24 formularios, conserva salidas de modelo defectuosas como revisables y escapa contenido no confiable. La comprobación visual usa una campaña temporal explícita, distinta del alumno, y se restaura su selección al finalizar.

## Repetir

```bash
python3 -m unittest discover -s tests -v
node tests/advanced-ui.mjs
docker compose --profile '*' config --format json | python3 scripts/verify_compose.py
./lab.sh up
./lab.sh php-on
./lab.sh ai-on
python3 -m tests.integration_continuation --full
```

La ruta de CI usa `python3 -m tests.integration_continuation` sin `--full`: ejecuta 19 objetivos reales y omite cinco dependientes de IA mediante **premios fixture identificados**, sin generar inferencias ni eventos falsos. El informe completo local exige las tres inferencias reales. No confundir ambos alcances.

El hash del expediente específico se calcula con JSON `sort_keys=True`, `ensure_ascii=False`, separadores `(',', ':')`, UTF-8, sin incluir el evento de su propia exportación. El expediente general de `/api/export` tiene su propia serialización documentada en el servidor. Ninguno es una firma resistente al administrador del anfitrión.

## Límites prácticos

Se ejecutó en macOS ARM64 con más memoria física que la referencia del alumno. Los manifiestos fijados incluyen ARM64 y AMD64; no se realizó aquí una ejecución nativa AMD64 ni PowerShell/Windows. El piloto físico de **16 GB sin GPU sigue pendiente**. Los límites configurados no miden un pico real ni garantizan margen del sistema anfitrión.

El nivel implementado de PHP2Shell es inventario, cambio real de despliegue y regresión funcional. **No se ejecutaron los PoC RCE de las dos CVE**. La sonda no demuestra explotación ni corrección exhaustiva de todas las rutas. El despliegue antiguo permanece aislado para la reversión del guion. La restauración comprueba un documento sintético, no la recuperación integral de una organización.

Las empresas, impactos, condición OIV y autoridad representada por estudiantes son ficticios. La plataforma comprueba hechos y estructura; no califica automáticamente criterio profesional, aceptación de riesgo ni cumplimiento legal. La defensa pública sigue siendo formativa; el único examen final se prepara fuera del repositorio.

En la revisión del navegador se comprobó un formulario completo con evidencia real y avance al siguiente objetivo. Una inferencia adicional del caso visual apareció por actualización automática y conservó un borrador que ya estaba escrito. El escritorio noVNC conectó con el puesto de análisis y mostró la guía de los nuevos comandos. La captura `docs/assets/asistente-local.png` procede de ese caso temporal, con premios anteriores identificados como fixtures; no es progreso de un estudiante.
