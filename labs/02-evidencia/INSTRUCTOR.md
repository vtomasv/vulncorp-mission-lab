# Instructor · Clase 2

[Guía y agenda](ESTUDIANTE.md). Preparar previamente Syft, Grype y su base, conservar el estado de la base y no esperar el mismo conteo de un scanner entre fechas.

## El contraste que debe ocurrir

La biblioteca más grave del expediente no es necesariamente la exposición con mayor consecuencia. El scanner detecta un componente realmente instalado; la investigación de uso y la evidencia de aplicación aportan información diferente.

## Respuestas de referencia

| Entrada | Conclusión defendible |
|---|---|
| F-01 | Django 3.2 está presente y la versión figura afectada. El servicio activo no usa el framework; no hay ruta demostrada en la revisión. Registrar límites y revisar al cambiar la aplicación. |
| F-02 | Falla local de autorización reproducible, sin CVE de proveedor. Mantener en gestión aunque no aparezca en el SBOM. |
| F-03 | Configuración y acceso de cuenta compartida. Catalogar copias no demuestra restauración. |
| F-05 | requests afectado está presente; el advisory tiene condiciones de uso. No se importa en el servicio actual. |
| VENDOR-06 | Duplicado docente de F-01 por activo + componente + versión + CVE. |
| VENDOR-07 | Atribución sintética incorrecta a mission, que no instala ese paquete; usar su SBOM propio. |

`present_not_reachable` se usa como etiqueta interna de investigación del curso; no es un estado VEX oficial ni equivale a `not_affected`. `false_positive` exige justificar el matching o la atribución errónea, no ausencia de explotación.

## Conducir los 110 minutos A

1. Exportar imágenes y generar ambos SBOMs.
2. Pedir localizar paquete, versión y purl.
3. Contrastar contra el contenido de cada imagen.
4. Ejecutar scanner y conservar su origen.
5. Leer advisory, no solo score.

En B: seis entradas como núcleo, las siete y otras coincidencias reales como extensión. No exigir una cantidad fija de CVEs de sistema operativo. No modificar el ejercicio para hacer coincidir un número de alertas cambiante.

## Debate de 80 minutos

La mitad de los equipos representa al proveedor y recibe un reporte incompleto; la otra mitad representa al cliente. Deben pedir y ofrecer la evidencia mínima para una conclusión. Luego intercambian roles y señalan qué información les hizo revisar una decisión.

## Continuidad

Si falla la descarga, el SBOM sigue siendo un resultado real. Para discusión se puede usar el expediente curado claramente identificado, o un reporte auténtico previamente generado con su hash y fecha. No describir ese modo como un nuevo escaneo en vivo.

## Cierre

Pedir a cada persona una frase que usaría en un informe y otra que rechazaría por exceder evidencia. Exportar expediente y archivos de scanner por separado. Sin calificación.
