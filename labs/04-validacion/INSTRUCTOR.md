# Validación · guía docente

Propósito: que el estudiante diseñe una prueba proporcional, distinga fuerza de evidencia y defienda una conclusión reproducible. Preparar `up`, `webscan-on` y modelo/base ya usados en la campaña. El núcleo funciona offline tras precarga; las lecturas externas pueden prepararse antes de la sesión.

## Qué se ejecuta y qué se simula

La autorización defectuosa, la versión corregida, el callback entre contenedores, el subproceso fijo y el análisis pasivo ZAP son reales. Los expedientes, empresas, identidades y efectos del negocio son sintéticos. El marcador es un instrumento explícito de medición; no se enseña como reproducción de Log4Shell. Mantener esta distinción en la demostración y las futuras PPT.

La corrección de R-01 no cambia F-02 ni su mitigación previa. El gemelo `vuln` permanece defectuoso por diseño; el gemelo `fixed` comprueba tenant desde el inicio; `live` se modifica en la zona siguiente. Nunca interpretar estos gemelos como un despliegue de producción.

## Secuencia pedagógica

Antes del terminal: pedir una hipótesis falsable, matriz esperada, permiso y criterio de detención. Modelar una sola fila con `curl`; el estudiante completa el resto. Después del terminal: pedir hechos separados de inferencias y una contraprueba propuesta por otro equipo. Retirar gradualmente los ejemplos sin penalizar el uso de pistas.

La base guiada no pretende ocupar una jornada completa. La profundidad está en construir la matriz bidireccional, investigar el método WSTG, revisar un caso documentado, contrastar alertas y defender el dictamen ante un dueño. No usar espera artificial ni repetir comandos para llenar tiempo. Si falta dominio conceptual, continuar el recorrido en la siguiente sesión; no hay cuenta regresiva en la plataforma.

## Intervenciones que revelan comprensión

| Error productivo | Pregunta y contraprueba |
|---|---|
| «El callback confirma RCE». | ¿Dónde está el proceso? Comparar las dos ejecuciones y sus eventos. |
| «200 demuestra éxito de seguridad». | ¿De quién es el objeto? Cambiar solo identidad y conservar documento. |
| «403 arregla todo». | ¿El dueño legítimo sigue recibiendo 200? Probar ambos clientes. |
| «ZAP no lo alertó; no existe». | ¿Cómo obtuvo ZAP la regla de propiedad del negocio? Mostrar la lectura manual. |
| «Esto reproduce MOVEit». | Contrastar la falla real SQLi del caso y la autorización de objetos de este laboratorio. Son mecanismos distintos. |

## Criterios de revisión sin nota

Comprobar que el dictamen permite repetir la prueba, conserva controles positivos/negativos, cita IDs y no exagera. Discutir si el criterio de detención es observable y quién puede autorizar una ampliación. La plataforma valida estructura y evidencias; no sustituye esta conversación.

## Recuperación

`lab abrir` es idempotente para la campaña actual. El episodio, los controles y los registros del nuevo rango se guardan en el volumen `range_state`: reiniciar o recrear sus contenedores conserva la continuidad. Solo una campaña nueva abre otro episodio; las fuentes del anterior quedan históricas. El historial no se borra. No usar una nueva campaña como solución automática. Las pruebas de desarrollo usan una campaña de fixture claramente rotulada y restauran la selección anterior.

ZAP usa imagen oficial multiarch fijada por digest y memoria máxima de 768 MiB. Se inicia bajo demanda, sin puertos al host ni Internet en la red de práctica. No habilitar escaneo activo para «hacerlo más interesante»; la pregunta del negocio ya permite un contraste potente.
