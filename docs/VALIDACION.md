# Validación de la campaña · versión 0.2.0

Fecha: **20 de octubre de 2026**. Se distingue configuración, ejecución funcional y pilotaje pendiente.

## Comprobaciones realizadas

| Comprobación | Resultado |
|---|---|
| Pruebas unitarias | 43 correctas: 72 ramas SSVC oficiales, contexto, presupuesto, referencias IA y de evidencia; además desbloqueos, puntos únicos, campañas separadas, firma alterada, actor incorrecto y pruebas posteriores al cambio. |
| Campaña integrada | Los 15 objetivos completados con 1370 PX; reintentos sin duplicar puntos. Comandos reales desde análisis y por SSH, Syft/Grype, IA local, revisión y residual. |
| Escritorio real | Chrome → noVNC → Linux UID 1000 → evidencia recogida → avance. SSH con terminal interactiva probado en soporte y aplicaciones. |
| Perspectivas | Análisis: gateway. Soporte: gateway/backup. Aplicaciones: gateway/records. También se comprobó denegación por IP directa desde análisis hacia redes que no comparte. |
| Protección de procedencia | student no puede leer secretos ni diario privado. Pruebas del plano de gestión no acreditan al puesto. La identidad firmada incluye todas sus interfaces, no solo la IP que resuelve el DNS. |
| Inventario real | Syft 1.55.0 encuentra Django 3.2 y requests 2.31.0 en el snapshot parcial de records, ausentes en el snapshot del runtime mission. |
| Escaneo real | Grype 0.121.0 recibe un SBOM recién generado y encuentra los alias CVE-2021-35042 y CVE-2024-35195; conserva descriptor/base, hash y reporte. No se exige un conteo fijo. |
| IA local | Qwen3 1.7B real, digest verificado, CPU sin GPU. Consultas de 23,28 s y 20,85 s en ejecuciones de esta campaña; no son una promesa de latencia. |
| Cierre | Exportación 403, transacción completed posteriores al cambio, restricción vigente y residual con ambas referencias. Un 403 aislado no basta. |
| Compatibilidad funcional | El smoke previo sigue pasando: transacción, exposición, mitigación, continuidad, rotación, decisiones y exportación. |

La revisión de navegador cubre los comandos a través de noVNC y los formularios de proveedor, expediente, dos dueños, revisión IA, cartera y residual. Las capturas de [ruta](assets/mission-control.png), [puesto](assets/workstation-proof.png) y [móvil](assets/game-mobile.png) acompañan esta edición. El registro de desarrollo se conserva localmente en `artifacts/`; esos archivos de ejecución no se publican automáticamente.

## Recursos

Presupuesto configurado del juego con IA: **6752 MiB** de límites combinados, más sobrecarga Docker. Referencia: Docker con 8 GiB en host de 16 GB; dos CPU para IA, un modelo y una consulta. Puestos y targets permanecen activos durante la inferencia.

Entorno de validación: Docker Desktop Linux **ARM64**, motor 29, con más RAM física que el equipo objetivo. En las mediciones, escritorio alrededor de 79 MiB en reposo y aproximadamente 98 MiB de pico cgroup; soporte y aplicaciones alrededor de 19 MiB antes del escaneo. El cgroup de aplicaciones alcanzó su límite de 1280 MiB durante el escaneo, con reclamación de caché y **cero eventos OOM/oom_kill**. Ollama registró un pico cgroup de 3.420.774.400 bytes, aproximadamente 3,19 GiB, bajo su límite de 4 GiB. Las métricas de cgroup incluyen memoria que Docker Stats puede descontar como caché; no se suman picos de fases distintas como si fueran simultáneos.

**Pendiente:** piloto en equipo físico de 16 GB, Windows PowerShell, matriz completa de navegadores y prueba con principiantes para ajustar los tiempos. El éxito técnico no acredita comprensión ni duración pedagógica.

## Reproducir

Preparar antes con `./lab.sh prepare-game`. Luego, para desarrollo:

```bash
python3 -m unittest discover -s tests -v
docker compose --profile '*' config --format json | python3 scripts/verify_compose.py
./lab.sh smoke
python3 tests/integration_game.py
python3 tests/integration_game.py --full
```

El núcleo de integración no descarga IA ni base de escáner. `--full` requiere ambas preparadas y ejecuta las quince metas. Crea una **nueva campaña**, preservando las anteriores; no ejecutarlo durante una partida que quieras mantener activa.

La prueba de UI opcional requiere Playwright en el equipo de desarrollo:

```bash
LAB_UI_FULL=1 PLAYWRIGHT_CHANNEL=chrome node tests/ui.mjs
```

Puede indicarse `PLAYWRIGHT_PATH` para una instalación existente. Los alumnos no necesitan Node o Playwright. El test crea una campaña y conserva captura en caso de fallo. Comprueba progreso desde la red real y no desde un terminal simulado con texto HTML.

La [automatización pública](https://github.com/vtomasv/vulncorp-mission-lab/actions/workflows/ci.yml) prueba Linux AMD64: unidades, contrato de red, construcción de puestos, smoke, cinco objetivos con evidencia real, SSH interactivo y perspectivas de red. No descarga el modelo ni acredita inferencia en CI; esa ejecución se valida localmente por separado.

La figura Anatomy se conserva como recurso complementario, fuera de la ruta principal. Su auditoría de geometría sigue pasando; no se confunde con la comprobación del juego.
