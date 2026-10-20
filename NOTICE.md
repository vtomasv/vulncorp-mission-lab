# Procedencia y licencias

Autor del código y material original del curso: **Tomás Vera**, `vtomasv`, 2026. Código y guías originales bajo MIT. No hay logotipos oficiales ni atribución de respaldo de terceros.

## SSVC

`data/ssvc/deployer.json` y `human-impact.json` son copias sin modificar de los archivos de datos de [CERTCC/SSVC](https://github.com/CERTCC/SSVC), commit **8728fb326abfde5cc59f743f3758531c65b439db**:

- `data/json/decision_tables/ssvc/deployer_patch_application_priority_1_0_0.json`
- `data/json/decision_points/ssvc/human_impact_2_0_2.json`

Conservan **copyright 2026 Carnegie Mellon University** y su licencia MIT (SEI)-style, copiada íntegramente en [data/ssvc/LICENSE](data/ssvc/LICENSE). No se redistribuye la documentación de upstream bajo una licencia distinta. El árbol Deployer usa salidas Defer / Scheduled / Out-of-Cycle / Immediate. El árbol CISA Coordinator es otro modelo y no se mezcla con este.

## Software de terceros

Las imágenes base y herramientas se descargan con tag y digest fijados. Los paquetes del escritorio se instalan desde Debian Bookworm; sus versiones se registran en la imagen, sin afirmar una construcción bit a bit reproducible. No se redistribuyen binarios dentro de Git:

| Componente | Proyecto / licencia principal |
|---|---|
| Python | [python.org](https://www.python.org/psf/license/) / PSF |
| Syft, Grype | [Anchore](https://github.com/anchore) / Apache-2.0 |
| Ollama | [ollama/ollama](https://github.com/ollama/ollama) / MIT |
| Qwen3 1.7B | [Qwen3](https://qwenlm.github.io/blog/qwen3/) / Apache-2.0, consultar licencia del modelo exacto |
| Django 3.2 | [Django](https://github.com/django/django) / BSD-3-Clause |
| noVNC | [noVNC](https://github.com/novnc/noVNC) / MPL-2.0; visor basado en su API pública |
| websockify | [websockify](https://github.com/novnc/websockify) / LGPL-3.0 |
| TigerVNC | [TigerVNC](https://github.com/TigerVNC/tigervnc) / GPL-2.0 y avisos del proyecto |
| Openbox, xterm, OpenSSH | Paquetes Debian con sus licencias y copyright en `/usr/share/doc` de la imagen |
| requests 2.31.0 | [Requests](https://github.com/psf/requests) / Apache-2.0 |

Las distribuciones base incluyen sus avisos y licencias. `requirements-legacy.txt` fija hashes de wheels obtenidos de PyPI. Los paquetes legacy son deliberadamente antiguos, no dependencias de la aplicación activa.

## Figura Anatomy

La figura de comparación de contexto, conservada como recurso complementario y fuera de la ruta principal del juego, se construye con **Anatomy**, copyright (c) 2026 Ryan, bajo MIT. Se conserva la [licencia original](scripts/vendor/anatomy/LICENSE), junto a los módulos de geometría y auditoría usados en desarrollo. `web/anatomy.css` procede del mismo kit; `web/context-figure.js` es su figura generada. La geometría y su integración con el caso son originales del curso. Los módulos de desarrollo no se cargan en el navegador ni se incorporan a la imagen runtime.

## Datos y marcos

- FIRST EPSS: atribución a FIRST y al proyecto EPSS; snapshot real con fecha/origen en `data/intelligence.json`. [Datos y uso](https://www.first.org/epss/data.html).
- CISA KEV: catálogo público de CISA; se conserva su versión y el subconjunto de CVEs consultado. La ausencia en el subconjunto no significa seguridad.
- MITRE ATT&CK: IDs y enlaces como referencias a conductas y mitigaciones. No se reproduce una matriz completa ni se afirma mapeo oficial.
- ISO/IEC 27001:2022: solo numeración y referencias breves. No se reproduce el estándar; la interpretación debe contrastarse con una copia institucional licenciada.
- Normativa chilena: enlaces a BCN y ANCI, con alcance OIV exclusivamente simulado.

Los dossiers, costos, impactos, expedientes y fallas de la aplicación del curso son sintéticos. Los reportes de proveedor `VENDOR-06/07` son trampas didácticas, no reportes reales de terceros.

## Credencial pública de entrenamiento

El par Ed25519 en `training/ssh` es material original generado exclusivamente para la práctica y publicado por diseño. No contiene llaves de una instalación real, de GitHub ni del docente. Su privada se ofrece también en la interfaz; solo se autoriza para student en la entrada local del laboratorio. Las privadas internas por instalación y secretos de verificación no forman parte del repositorio.
