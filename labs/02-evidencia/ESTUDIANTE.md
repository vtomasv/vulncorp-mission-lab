# Clase 2 · El ruido y la señal

**Duración:** 7 horas efectivas. **Evaluación:** sin nota. **Punto de partida:** entorno y expediente de la clase 1.

## Tu encargo

El proveedor informa «siete vulnerabilidades». Su reporte mezcla componentes afectados, fallas locales, un duplicado y un activo mal atribuido. No puedes convertir automáticamente ese número en una agenda de parcheo.

El caso instala realmente **Django 3.2** y **requests 2.31.0** en `/opt/legacy` de la imagen records. La aplicación que atiende peticiones usa Python estándar y no importa esos paquetes. Debes comprobar presencia y uso por separado.

## Agenda

| Min | Actividad |
|---:|---|
| 20 | Predecir qué verá un SBOM y qué verá un scanner. |
| 40 | CVE, CWE, purl, versión y vector CVSS; presencia, afectación y alcanzabilidad. |
| 30 | Demostración Syft → Grype → advisory → límite de la conclusión. |
| 110 | Laboratorio A: generar SBOM y escanear imágenes exactas. |
| 110 | Laboratorio B: clasificar seis entradas y contrastar una falla sin CVE. |
| 80 | Proveedor vs analista: evidencia incompleta, decisiones y contraprueba. |
| 30 | Reflexión, exportación y transferencia. |

## Laboratorio A · Inventario y scanner reales

### Paso 1. Vuelve al perfil de targets

```bash
./lab.sh ai-off
./lab.sh status
```

Windows: `.\lab.ps1 ai-off`. Reiniciar targets devuelve su configuración defectuosa inicial; la bitácora histórica se conserva. No interpretes una evidencia anterior como si describiera necesariamente el estado actual.

### Paso 2. Genera dos SBOM

```bash
./lab.sh sbom
```

En Windows: `.\lab.ps1 sbom`. La primera ejecución descarga Syft. El script exporta imágenes a `artifacts/images/`, las monta **solo lectura** en Syft y no entrega el socket de Docker al scanner.

Archivos esperados:

- `artifacts/sbom-records.cdx.json`
- `artifacts/sbom-mission.cdx.json`
- `artifacts/syft-version.txt`

Abre ambos JSON en un editor de texto. Busca `Django`, `requests`, `purl`, `version` y `bomFormat`. En records aparecen los dos paquetes legacy; en mission no. El SBOM puede contener muchos paquetes del runtime y de Debian. Es software instalado, no una lista de vulnerabilidades.

**Pregunta:** ¿por qué importa el digest o identidad de la imagen cuando el proveedor te envía un SBOM?

### Paso 3. Confirma desde el contenedor

```bash
docker compose exec records python -c "from importlib.metadata import distributions; print([(d.metadata['Name'],d.version) for d in distributions(path=['/opt/legacy'])])"
docker compose exec mission python -c "from pathlib import Path; print(Path('/opt/legacy').exists())"
```

La primera salida contiene Django 3.2 y requests 2.31.0; la segunda debe ser `False`. Estos comandos también funcionan en PowerShell. Todavía no has demostrado que una función vulnerable sea usada por el servicio.

### Paso 4. Ejecuta Grype

```bash
./lab.sh scan
```

Windows: `.\lab.ps1 scan`. Grype descarga su base en un volumen separado. Solo el scanner tiene esa red de actualización; los targets continúan en redes internas.

Se generan `artifacts/grype-records.json` y `artifacts/grype-db-status.txt`. El conteo real **puede cambiar** al actualizarse la base. No debe coincidir con las siete tarjetas sintéticas del caso. Registra versión y fecha de la base y conserva el reporte.

### Paso 5. Importa sin confundir fuentes

En **Hallazgos**, selecciona el archivo `grype-records.json`. La UI guarda conteo, coincidencias Django/requests, descriptor y hash. No reemplaza las tarjetas del caso por datos inventados de Grype.

Busca CVE-2021-35042 en el reporte. Grype puede usar un identificador GHSA en `vulnerability.id` y el CVE en `relatedVulnerabilities`; son alias del aviso, no dos vulnerabilidades independientes por esa sola razón. La importación conserva ambos. Pueden aparecer otros advisories de Django o requests; eso no invalida el ejercicio. Si la base no carga, conserva el SBOM, usa el expediente docente **rotulado como tal** y programa la ejecución real cuando la descarga esté disponible.

## Laboratorio B · Investigar aplicabilidad

### Paso 6. F-01: componente crítico, ¿riesgo inmediato?

Lee [el aviso del mantenedor Django](https://www.djangoproject.com/weblog/2021/jul/01/security-releases/). Describe un posible SQL injection al usar entrada no saneada en `QuerySet.order_by()`. El fix de la rama 3.2 fue 3.2.5; eso no convierte esa versión histórica en recomendación general actual.

Revisa `app/targets.py`: el servicio activo usa la biblioteca estándar y no importa Django. Comprueba la ubicación `/opt/legacy` con los comandos anteriores.

Conclusión proporcional: **el componente afectado está presente; no se ha demostrado una ruta de uso de la función vulnerable**. No escribas «no es vulnerable» ni declares `not_affected` solo por estar en una red interna.

### Paso 7. F-05: condiciones de uso

Consulta [el advisory de requests](https://github.com/psf/requests/security/advisories/GHSA-9wx4-h78v-vm56). La condición se relaciona con una `Session` que inicia una conexión con `verify=False`. La aplicación activa no usa esa dependencia. Explica qué pregunta respondería la revisión de código y cuál respondería un scanner.

### Paso 8. Identifica el duplicado

Compara F-01 y VENDOR-06: activo, paquete, versión y CVE. En **Clasificar con evidencia**, elige **Duplicado de otro hallazgo** (`duplicate`) para VENDOR-06 y explica la coincidencia. Mismo CVE en **otro activo** no sería necesariamente el mismo trabajo de remediación: no dedupliques solo por CVE.

### Paso 9. Impugna la atribución incorrecta

VENDOR-07 atribuye requests al centro de misión. Usa su **SBOM propio**, no el de records, para cuestionarlo. Clasifica como **Atribución o coincidencia incorrecta** (`false_positive`) y evidencia concreta. No justifiques el estado diciendo «no fue explotado».

### Paso 10. Recupera la falla sin CVE

Repite `./lab.sh probe public export` y la prueba desde el mapa. F-02 no tiene CVE de un proveedor: es una falla local intencional de autorización. Su score y vector son una valoración docente explícita. No necesitas un CVE para gestionar esa exposición.

Completa una tabla con F-01, F-02, F-03, F-05, VENDOR-06 y VENDOR-07: fuente, activo, condición, evidencia, conclusión y confianza. F-04 y más discrepancias del reporte real son extensión.

## Comité y salida

El equipo proveedor debe defender una afirmación con su reporte. El equipo analista debe pedir la imagen, versión, fecha y condición faltante. Después intercambian roles.

Completa las reflexiones de Clase 2 y exporta expediente más reportes reales de `artifacts/`.

**Éxito observable:** distingues SBOM, scanner y validación; no confundes las tarjetas del caso con una salida real; identificas duplicado y atribución errónea; conservas una falla sin CVE en la gestión.

**Ayudas:** primero pregunta «¿en qué imagen?»; luego «¿qué paquete y versión?»; finalmente «¿qué condición de uso habilita el escenario?». Si cambian los conteos, compara las fuentes y sus fechas antes de cambiar de herramienta.
