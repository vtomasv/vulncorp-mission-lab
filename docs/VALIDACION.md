# Validación de la release 0.1.0

Fecha de la edición: **20 de octubre de 2026**. Este archivo distingue el contrato configurado de las comprobaciones realmente ejecutadas. Los siguientes resultados corresponden a ejecución real, con datos sintéticos; no son objetivos estimados.

## Contrato de recursos

- Base: mission 256 MiB, tres targets de 160 MiB cada uno; límite combinado 736 MiB.
- Syft y Grype: un proceso por turno, 1 GiB cada uno; extracción de imágenes y preparación de bases en volúmenes temporales de disco, no tmpfs de RAM.
- Inferencia: Qwen3 1.7B, 2 CPU, límite 4 GiB, sin GPU, máximo un modelo y una consulta.
- Targets pausados durante la inferencia. Centro de misión y evidencia disponibles.
- Los límites de contenedor no incluyen sobrecarga de la VM Docker, caché de páginas del host ni otras aplicaciones. Se recomienda pilotar el equipo completo de 16 GB antes de dictar.

## Resultados observados

Entorno local: Docker Desktop Linux **arm64**, motor 29, con más RAM disponible que el equipo objetivo. Los límites anteriores sí estuvieron activos. **No se ha pilotado una máquina física de 16 GB**, Windows PowerShell ni una cohorte; esa validación sigue pendiente.

| Comprobación | Resultado |
|---|---|
| Pruebas unitarias en host y contenedor | 25 correctas; incluyen las 72 combinaciones oficiales SSVC, cambio de contexto, restricciones de cartera, evidencia y trazabilidad de IA. |
| Flujo integrado | Transacción completada, exportación inicialmente 200, control aplicado, exportación 403 y transacción todavía completada. Rotación rechaza la llave previa. |
| Dos perspectivas de red | Desde public solo gateway; desde support solo backup. Contrato Compose: targets/IA internos, publicación loopback, sin socket Docker. |
| Syft real | Django 3.2 y requests 2.31.0 presentes en records; ausentes en mission. |
| Grype real | 330 coincidencias totales, 41 de Django/requests en la base consultada. Se encontraron los alias CVE-2021-35042 y CVE-2024-35195 y se importaron en la aplicación. El conteo no es estable entre fechas. |
| Base Grype | v6.1.10, construida 2026-10-20 06:29:49 UTC; estado válido. |
| IA local | Qwen3 1.7B, digest verificado contra el lock; solicitud completa guardada; 20,66 s y 277 tokens de salida en la consulta de referencia. |
| RAM de IA | Pico cgroup de Ollama: 2.067.271.680 bytes, aproximadamente 1,93 GiB; máximo muestreado por Docker Stats: 1,858 GiB. Son métricas distintas; no incluyen toda la VM del host. |
| Revisión humana | Se corrigió la afirmación no justificada «riesgo alto» y la confusión de hipótesis con observación. El validador estructural había pasado. |
| Interfaz | Navegación, prueba real, guardado de reflexión/decisión, cambio de cliente y vista IA en navegador de escritorio y móvil; sin errores de consola ni desborde horizontal global. |
| Persistencia | Las decisiones y evidencias sobrevivieron a la recreación del contenedor mission. Las pruebas también comprueban reapertura de SQLite e integridad del hash exportado. |

La consulta y su revisión completas están en [el ejemplo capturado](ejemplos/inferencia-cpu.json). Es una captura de validación, no una respuesta que la aplicación use para aparentar inferencia.

La automatización pública ejecuta las pruebas funcionales en Linux **amd64** sin descargar el modelo. La [primera ejecución](https://github.com/vtomasv/vulncorp-mission-lab/actions/runs/39467440045) pasó: pruebas unitarias, contrato Compose, construcción, flujo integrado y descubrimiento desde dos zonas. Consulta las [ejecuciones posteriores](https://github.com/vtomasv/vulncorp-mission-lab/actions/workflows/ci.yml) para el estado actual; una insignia verde no acredita pruebas de IA, Windows ni hardware de 16 GB.

## Pruebas reproducibles

```bash
./lab.sh test
docker compose --profile '*' config --format json | python3 scripts/verify_compose.py
./lab.sh up
./lab.sh smoke
./lab.sh discover public
./lab.sh discover support
./lab.sh sbom
./lab.sh scan
./lab.sh ai-prepare
./lab.sh ai-on
```

El segundo comando es una verificación de desarrollo/CI: usa Python en el host. No es requisito para los alumnos; las pruebas funcionales se ejecutan en Docker con el lanzador.

`smoke` crea observaciones de entrenamiento y devuelve los targets a su estado inicial. El reporte real de Grype no tiene un conteo estable entre fechas. El test de UI opcional requiere Playwright en el equipo de desarrollo, no en el equipo del estudiante.

## Plataformas

Las imágenes fijadas anuncian soporte Linux amd64/arm64. Anunciar una arquitectura no equivale a haber probado toda la guía en ese sistema operativo. La validación de PowerShell y el pilotaje pedagógico en una cohorte se deben registrar por separado; el cumplimiento técnico no prueba duración ni comprensión del alumno.

## Datos que se conservan con una comprobación

Versiones y digests; sistema/arquitectura; límite de recursos; pico observado y fase; estado de base Grype; reporte; modelo/digest; latencia de inferencia, salida y revisión; pruebas antes/después de un control; captura de escritorio y móvil; estado de CI.
