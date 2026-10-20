# Solución de problemas

| Síntoma | Comprobación | Recuperación |
|---|---|---|
| Docker muestra solo Client | Motor apagado o contexto incorrecto. | Abrir Docker Desktop/Engine, esperar y ejecutar `doctor`. |
| Puerto 8095 ocupado | Otra aplicación usa ese puerto. | Copiar `.env.example` a `.env`, cambiar `LAB_PORT=8096`, repetir `up` y abrir el nuevo puerto. |
| No resuelve records desde public | Es la red esperada. | Probar transaction a través del gateway; no «arreglar» un aislamiento correcto. |
| Export devuelve 403 al inicio | Quedó una medida aplicada. | Revisar historial y usar `reset-targets` si el objetivo es volver al escenario inicial. |
| Transaction devuelve 503 | records está apagado o aún inicia. | `status`, después `ai-off` o `up`. Un 503 no demuestra mitigación. |
| Targets no aparecen en mapa | Puede estar activo el modo IA. | `ai-off`. Los targets reinician estado; repetir pruebas. |
| Syft no encuentra la imagen | No existe el archivo exportado o no se construyó. | Ejecutar `up`, después `sbom`. No montar Docker socket para resolverlo. |
| Grype no descarga la base | Red, proxy o servicio del feed. | Reintentar fuera del bloque docente; conservar SBOM y usar reporte auténtico fechado ya generado. El expediente del caso es otra fuente, rotulada. |
| Grype informa más alertas que la guía | La base cambia y el runtime contiene más paquetes. | Registrar fecha, versión e imagen; investigar los paquetes del ejercicio, sin forzar un conteo. |
| IA dice «sin modelo» | Descarga incompleta o nombre distinto. | `ai-prepare`, luego `ai-on`; comprobar `ollama list`. |
| IA tarda mucho | CPU compartida, contexto o modelo mayor. | Mantener 1.7B, solo un hallazgo, targets pausados y esperar la consulta antes de repetir. |
| Salida IA con referencia falsa | El ID no pertenece a sus fragmentos. | Corregir o rechazar; no aceptar solo porque está bien escrita. |
| PowerShell bloquea script | Política de ejecución. | Usar una política de proceso si está permitido o los comandos Docker directos de INICIO. |
| Acentos incorrectos en reportes | Redirección de Windows PowerShell 5. | Usar `lab.ps1`, que escribe UTF-8 sin BOM. No redirigir reportes con `>` en esa versión. |

## Recuperación sin perder el expediente

`reset-targets` reinicia solo los tres servicios del caso. `down` detiene solo este proyecto y conserva volúmenes. Antes de un cambio exporta evidencia. Evita `docker system prune`, `docker volume prune` o `down -v`: no son pasos necesarios del laboratorio y pueden eliminar trabajo.

Los archivos `artifacts/images/*.tar` se pueden volver a generar con `sbom`. Ocupan disco pero no son necesarios para ejecutar el escenario ya construido. Conserva los JSON, metadatos y hashes que uses como evidencia.

Los tiempos de primera descarga dependen de la red. El docente debe precargar imágenes, base y modelo. Las afirmaciones de rendimiento se consultan en [VALIDACION](VALIDACION.md), separando lo probado de lo recomendado.
