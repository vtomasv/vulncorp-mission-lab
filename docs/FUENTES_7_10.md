# Fuentes y límites del tramo final · consulta 21 octubre 2026

| Fuente primaria | Hecho documentado y adaptación |
|---|---|
| [PHP · CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w) | Corrupción asociada a falta de memoria, con condiciones dependientes de SAPI e inicio/limpieza. Se analizan condiciones y actualización; el laboratorio no reproduce su RCE. |
| [PHP · CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp) | Estado global conserva referencias entre solicitudes; la cadena descrita exige condiciones específicas de productor/consumidor. Desactivar progreso de carga cubre una condición, sin sustituir la actualización. No es una webshell genérica. |
| [PHP · anuncios 2026](https://www.php.net/archive/2026.php) | La comparación de la rama 8.4 usa 8.4.26 y la corrección 8.4.27. La disponibilidad de una imagen no prueba que el servicio activo la use. |
| [Docker Library PHP](https://github.com/docker-library/php) | Bases oficiales Apache/mod_php. Versiones y digests multiarch fijados en `data/php-images.json`; las capas locales añaden únicamente la aplicación y configuración del laboratorio. |
| [Ollama · salidas estructuradas](https://docs.ollama.com/capabilities/structured-outputs) | Contrato de salida comprobable. Un esquema válido no garantiza veracidad ni correspondencia entre fuente y afirmación. |
| [OWASP · Prompt Injection](https://genai.owasp.org/glossaries/prompt-injection/) | Marco para discutir instrucciones no confiables. La nota del proveedor es una simulación original, no la reproducción de un incidente real atribuido a una empresa. |
| [NHS England · Synnovis](https://www.england.nhs.uk/synnovis-cyber-incident/questions-and-answers/) | Disrupción de un proveedor y efectos en función clínica. Inspira la pregunta de continuidad; no se atribuye al incidente la falla PHP del rango ni su mecanismo de acceso. |
| [GAO · Equifax 2017](https://www.gao.gov/assets/gao-18-559.pdf) | Caso documentado para cuestionar cobertura de inventario y efectividad del proceso de parcheo. El portal y la reversión de ruta son ficticios, no una reconstrucción de su infraestructura. |

Los resúmenes del juego son paráfrasis breves fechadas, conservadas en `data/continuation.json`; las observaciones del rango tienen IDs y procedencia propia. Los avisos pueden cambiar: antes de otra edición se deben contrastar condiciones, versiones y limitaciones con sus fuentes. Este repositorio no congela una copia íntegra de las páginas ni afirma una reproducción bit a bit de las imágenes locales.

Para [MITRE, ISO y derecho chileno](FUENTES_4_6.md) se reutiliza el alcance y fecha del caso anterior. No se agregan nuevas reglas de plazo o vigencia en este tramo. La empresa OIV es un supuesto expreso; una vulnerabilidad no prueba por sí sola un incidente significativo. T1190 puede orientar la amenaza, pero estas pruebas no observan explotación RCE. A.8.8 y A.8.13 no son certificados de cumplimiento ni sustituyen la lectura de un ejemplar ISO licenciado.
