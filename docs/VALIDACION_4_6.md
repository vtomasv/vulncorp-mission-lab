# Validación del tramo 4–6 · 21 octubre 2026

## Cobertura ejecutada

| Comprobación | Resultado |
|---|---|
| Pruebas unitarias del repositorio | 64 aprobadas, incluyendo plazos, referencias inventadas, episodios históricos, causalidad y persistencia |
| Recorrido nuevo por SSH desde el host | 18/18 objetivos nuevos, gateway real, API vulnerable/corregida y colector real |
| ZAP oficial | 2.17.0, cuatro solicitudes reales y análisis pasivo, reporte con hash |
| Marcador | Subproceso fijo real y recibo del colector correlacionado; no reproducción de CVE |
| Autorización y revocación | Ensayos con tres identidades antes/después; bloqueo y acceso legítimo conservados |
| Persistencia del rango | Reinicio de validation/collector después de autorización; mismo episodio y control conservados; revocación posterior aprobada |
| Capa Navigator | Solo T1190/T1078, formato 4.5, IDs y análisis humano vinculados |
| IA local | Qwen3 1.7B CPU, digest verificado, inferencia real sobre pruebas actuales y fuente legal; revisión humana conservada |
| Regresión del primer tramo | Cinco primeros objetivos reales por SSH, con las redes y perspectivas originales conservadas |
| Acceso SSH | Llave publicada descargable, host verificado, UID 1000; rechazo de root, contraseña, otra llave y reenvío arbitrario |
| noVNC | Apertura del rango y callback ejecutados desde terminal gráfica real, formularios y fuentes guardados; dos objetivos nuevos avanzaron automáticamente |
| Configuración Docker | Puertos de entrada solo en loopback; rango/colector/ZAP solo internos; sin socket Docker ni privilegios generales |

La prueba de continuación usa una campaña separada con los **primeros quince hitos como fixture de prueba explícito**. No inventa pruebas para los dieciocho objetivos nuevos. Restaura la campaña seleccionada anteriormente y conserva toda la historia de validación. La comprobación visual también usa fixture y recibos reales noVNC para los dos objetivos indicados. La captura de `docs/assets/expansion-validacion.png` pertenece a esa campaña de prueba.

La inferencia de cierre observada tardó 29.64 s y produjo una referencia ausente o ajena a los fragmentos recibidos. El validador la detectó y la revisión se registró como corrección, no como aceptación. Se conserva como resultado real y ejemplo de por qué el modelo requiere revisión; no se declara que toda salida sea correcta por usar fuentes locales. El tiempo observado no es garantía para otros equipos.

## Hallazgo corregido durante la prueba prolongada

La primera configuración alojaba la carpeta de ZAP en un tmpfs de 96 MiB. Su base de trabajo creció y agotó ese espacio, terminando el proceso. Se cambió a un volumen de disco `zap_work`; el límite del contenedor se mantiene en 768 MiB. La carpeta observada ya ocupaba aproximadamente 176 MiB durante la repetición satisfactoria. Los logs del contenedor tienen rotación configurada.

Los límites del conjunto habitual suman 7744 MiB con IA y ZAP activos. Una captura de consumo durante inferencia queda como artefacto local de desarrollo; no equivale a medir un máximo ni a un piloto físico de 16 GB. La ejecución funcional se hizo en ARM64 con más RAM física. PowerShell/Windows y el piloto físico de 16 GB siguen pendientes.

## Reproducir

Con imágenes, base y modelo preparados:

```bash
python3 -m unittest discover -s tests -v
docker compose --profile '*' config --format json | python3 scripts/verify_compose.py
./lab.sh up
./lab.sh webscan-on
python3 -m tests.integration_ssh
python3 -m tests.integration_advanced --full
```

Sin `--full`, la prueba de continuación recorre 17 objetivos y deja sin ejecutar la inferencia real final. La integración continua usa esa modalidad; no declara una inferencia local en el runner si no descargó sus pesos. Los archivos bajo `artifacts/` quedan fuera del repositorio por ser salidas de ejecución, no material precargado para simular resultados.

El código de pruebas es para desarrollo/docencia. Las guías del alumno no otorgan PX mediante fixture. La plataforma comprueba fuentes, estados y estructura; la comprensión, proporcionalidad del argumento y autoridad del dueño se revisan en discusión. No hay nota por estos hitos.

Una prueba de restauración detectó y corrigió una debilidad del núcleo anterior: observaciones posteriores podían completar una campaña más antigua al retomarla. Los registros nuevos se vinculan al intervalo activo de campaña y el verificador exige coincidencia de campaña cuando existe esa asociación. Se conservaron los registros de prueba y se restauraron los hitos de la campaña original desde el respaldo previo.
