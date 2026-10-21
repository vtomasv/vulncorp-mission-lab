# Hechos reales, adaptación ficticia y fuentes

## Equifax, 2017

Se usa para discutir inventario, responsabilidad de parcheo y verificación efectiva. La fuente es el [informe primario GAO-18-559](https://www.gao.gov/assets/gao-18-559.pdf). El portal de este repositorio no es Equifax ni reproduce su infraestructura. El caso muestra cómo un reporte o un parche publicado no garantizan cobertura o cierre.

## MOVEit/CL0P, 2023

El [aviso oficial CISA/FBI AA23-158A](https://www.cisa.gov/sites/default/files/2023-06/aa23-158a-stopransomware-cl0p-ransomware-gang-exploits-moveit-vulnerability_7.pdf) describe explotación de MOVEit. Aquí se representa el problema de exposición y transferencia entre clientes con una aplicación original abierta. **La falla local de autorización no es CVE-2023-34362** ni pretende reproducir el SQL injection de MOVEit.

## Trivy, marzo de 2026

El [informe de Aqua, mantenedor de Trivy](https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know/) se usa para discutir confianza en herramientas y tags mutables. Esta release utiliza Syft/Grype fijados por digest; no incluye una versión comprometida de Trivy ni código malicioso de ese incidente.

## CVEs realmente presentes como componentes

- [Django: CVE-2021-35042](https://www.djangoproject.com/weblog/2021/jul/01/security-releases/): Django 3.2 en `/opt/legacy`, sin importación en el servicio activo.
- [requests: CVE-2024-35195](https://github.com/psf/requests/security/advisories/GHSA-9wx4-h78v-vm56): requests 2.31.0 en la misma ubicación. Las condiciones de uso se investigan; no se prueba el exploit en estas clases.

Los hashes de wheels se obtuvieron de PyPI y están en `requirements-legacy.txt` y `data/packages-provenance.json`. Los reportes reales de Grype pueden encontrar otros advisories. Las siete tarjetas del caso no se atribuyen al scanner.

## Priorización

- [FIRST CVSS v3.1](https://www.first.org/cvss/v3.1/specification-document), para interpretar los vectores de este conjunto. No se convierten a v4 de forma ficticia; se puede discutir v4 como extensión.
- [FIRST EPSS](https://www.first.org/epss/) y [datos](https://www.first.org/epss/data.html): snapshot real, fecha incluida. No es probabilidad local.
- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): versión y coincidencias conservadas en `data/intelligence.json`.
- [CERT/CC SSVC Deployer](https://certcc.github.io/SSVC/howto/deployer_tree/): datos oficiales en `data/ssvc`, con commit y licencia.

El índice ordinal `4×L×I` es una **política docente original**, no una fórmula de ISO, MITRE, FIRST ni una obligación legal. El máximo de impactos evita promediar un daño en personas con consecuencias menores, pero no convierte niveles ordinales en pérdidas monetarias.

## Controles, IA y Chile

- MITRE: [T1190](https://attack.mitre.org/techniques/T1190/), [T1078](https://attack.mitre.org/techniques/T1078/), [T1213.006](https://attack.mitre.org/techniques/T1213/006/); mitigaciones [M1051](https://attack.mitre.org/mitigations/M1051/), [M1026](https://attack.mitre.org/mitigations/M1026/), [M1030](https://attack.mitre.org/mitigations/M1030/), [M1053](https://attack.mitre.org/mitigations/M1053/).
- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001): A.8.8 vulnerabilidades técnicas; A.8.2 privilegios; A.8.13 copias; A.8.22 segregación; A.8.26 requisitos de aplicaciones; A.5.30 continuidad TIC. Referencias didácticas; contrastar numeración e interpretación con ejemplar licenciado.
- [Ley 21.663](https://www.bcn.cl/leychile/navegar?idNorma=1202434), especialmente gestión, revisión y continuidad OIV del art. 8; [Ley 21.459](https://www.bcn.cl/leychile/navegar?idNorma=1177743), para delimitar autorización y pruebas; datos exclusivamente ficticios.
- [Ollama Docker](https://docs.ollama.com/docker), [salidas estructuradas](https://docs.ollama.com/capabilities/structured-outputs), [Qwen3](https://qwenlm.github.io/blog/qwen3/).
- OWASP: [Prompt Injection](https://genai.owasp.org/glossaries/prompt-injection/) y [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).

Una técnica exige conducta observada; un control exige prueba; un artículo exige alcance y vigencia. No hay equivalencia automática entre CVE, ATT&CK, ISO y ley. Fecha editorial de la release: 20-10-2026; revisar normativa antes de otra edición.

La [continuación 4–6](FUENTES_4_6.md) amplía los casos Log4Shell, MOVEit y Synnovis con fuentes primarias y límites explícitos de la analogía. Incluye las referencias legales con fecha de caso 21 octubre 2026 y la distinción de vigencia de Ley 21.719.
