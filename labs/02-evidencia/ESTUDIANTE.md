# Señales · convierte alertas en un expediente

Necesitas la zona anterior acreditada. Desde el puesto de análisis entra a aplicaciones. Si sigues en soporte, ejecuta `exit` antes:

```bash
ssh appdesk
```

## 6. Inventario con procedencia

Predice qué demostraría encontrar un paquete, y qué no. Ejecuta:

```bash
lab inventario
jq '.components[] | select(.name=="django" or .name=="requests") | {name,version,purl}' ~/evidence/records.cdx.json
```

Syft encuentra Django 3.2 y requests 2.31.0. Son archivos reales copiados de records; el alcance es un snapshot parcial de solo lectura. No lo presentes como SBOM completo de toda la imagen.

## 7. Una alerta no es una decisión

```bash
lab escanear
jq '.descriptor' ~/evidence/grype-records.json
```

Grype recibe un inventario recién generado, usa la base precargada y conserva reporte, hash y alias CVE/GHSA. Localiza CVE-2021-35042 y CVE-2024-35195. El número total puede variar con la base; no tiene por qué ser siete ni coincidir con el catálogo sintético del proveedor.

## 8. Presente y utilizado

```bash
lab revisar
less /company/active-service/targets.py
```

Busca imports y compáralos con el inventario. Consulta los advisories enlazados en las fuentes del repositorio. Explica la conclusión proporcional: los componentes existen; esta revisión no demuestra una ruta de uso de su función vulnerable. Indica qué otra prueba podría cambiar tu conclusión.

## 9. Dos errores del proveedor

```bash
lab contrastar
```

Compara records y mission. En la ruta completa el formulario: ¿qué registro repite activo, versión y CVE? ¿Cuál atribuye requests al activo equivocado? Fundamenta usando procedencia y alcance; no elimines una alerta solo porque te molesta.

## 10. Un expediente defendible

Vuelve a la ruta. Clasifica F-01 y F-02, vincula la exportación auténtica y explica qué has demostrado. El tablero comprueba clasificaciones y referencias; tu equipo debe discutir si la explicación es suficiente.

## Defensa del equipo

Presenta tres frases: un hecho, una inferencia y una hipótesis pendiente. Otro equipo busca una fuente que las contradiga. Explica por qué una falla sin CVE puede merecer atención antes que una biblioteca con CVSS 9.8. Conserva los reportes en el hogar de aplicaciones y el expediente exportado.

Continúa en [Continuidad](../03-priorizacion/ESTUDIANTE.md).
