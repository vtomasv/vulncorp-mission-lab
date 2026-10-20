# VulnCorp Mission Lab

[![Laboratorios verificables](https://github.com/vtomasv/vulncorp-mission-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/vtomasv/vulncorp-mission-lab/actions/workflows/ci.yml)

**Gestionar vulnerabilidades es proteger un servicio y demostrar una decisión.**

Tres laboratorios intensivos del curso MAR303, creados por **Tomás Vera**. Una experiencia práctica en español, para estudiantes desde principiante, con Docker, herramientas abiertas e IA local en CPU. Equipos de referencia: **16 GB RAM, sin GPU**.

![Centro de misión: mapa operativo y contexto del cliente](docs/assets/mission-control.png)

## En cinco minutos, después de descargar imágenes

Requisitos del host: Git, Docker Engine + Compose v2 o Docker Desktop con backend Linux, y navegador. No necesitas Python, Node, Syft, Grype ni Ollama instalados en el host. La primera preparación requiere Internet; sus tiempos de descarga no son cinco minutos garantizados.

**macOS / Linux**

```bash
git clone https://github.com/vtomasv/vulncorp-mission-lab.git
cd vulncorp-mission-lab
./lab.sh doctor
./lab.sh up
```

**Windows PowerShell**

```powershell
git clone https://github.com/vtomasv/vulncorp-mission-lab.git
cd vulncorp-mission-lab
.\lab.ps1 doctor
.\lab.ps1 up
```

Abre **[http://localhost:8095](http://localhost:8095)**. Si Windows bloquea el script, consulta [Inicio para principiantes](docs/INICIO.md); también puedes usar directamente los comandos Docker que se documentan allí.

## El giro de la experiencia

1. **Una transacción real funciona.** Comprueba su dependencia y descubre una exportación sin autorización con expedientes completamente ficticios.
2. **El escáner no decide por ti.** Syft y Grype inspeccionan paquetes realmente instalados. Contrasta sus resultados con un expediente docente que incluye un duplicado y un falso positivo.
3. **Cambia el dueño, cambia la prioridad.** Salud, agua y servicios digitales comparten hallazgos, pero no consecuencias.
4. **Cuatro horas de ingeniería. Quince minutos de ventana.** Elige y justifica una cartera; el sistema comprueba restricciones.
5. **La IA necesita que la audites.** Ollama y Qwen3 proponen preguntas y tratamientos con fuentes locales. Un motor determinista calcula riesgo y SSVC.
6. **Demuestra que sirvió.** Restringe la exportación pública. Comprueba HTTP 403 y, a continuación, una transacción legítima completada. El registro distingue mitigación de corrección de causa raíz.

## Las tres clases

| Clase | Pregunta central | Guía del estudiante |
|---|---|---|
| 1 · Lo que no ves también decide | ¿Qué necesita seguir funcionando y desde dónde es accesible? | [Superficie, negocio y evidencia](labs/01-superficie/ESTUDIANTE.md) |
| 2 · El ruido y la señal | ¿Qué demuestra un scanner y qué requiere investigación? | [SBOM, CVEs y aplicabilidad](labs/02-evidencia/ESTUDIANTE.md) |
| 3 · La prioridad cambia de dueño | ¿Qué hacemos primero para este cliente y cómo lo comprobamos? | [Riesgo, SSVC, IA y tratamiento](labs/03-priorizacion/ESTUDIANTE.md) |

Cada jornada tiene **420 minutos de actividad**, incluidos dos bloques de laboratorio de 110 minutos y 80 minutos de contraste y decisión. Pausas y colación se programan aparte. Hay guías de instructor y ayudas progresivas. **Ningún laboratorio tiene nota, bono ni ponderación**; esta edición del curso contempla solo examen final, fuera de este repositorio de clases 1-3.

## IA local, de verdad

```bash
./lab.sh ai-prepare   # primera vez: descarga el motor y Qwen3 1.7B
./lab.sh ai-on        # inferencia CPU; pausa los tres targets
```

En Windows reemplaza `./lab.sh` por `.\lab.ps1`. En el centro de misión abre **IA local**. Para volver al escenario:

```bash
./lab.sh ai-off
```

La inferencia usa **un modelo a la vez, dos CPU y un límite de 4 GB**. Las evidencias permanecen disponibles cuando los targets están pausados. Al volver, los targets reinician su estado: hay que volver a comprobar las mitigaciones. No se usa un servicio de IA cloud. El sistema muestra claramente si el modelo no está disponible; no genera respuestas ficticias en su lugar. [Cómo funciona, medición y límites](docs/IA_LOCAL.md).

## Herramientas y evidencia

```bash
./lab.sh discover public
./lab.sh discover support
./lab.sh probe public transaction
./lab.sh probe public export
./lab.sh sbom
./lab.sh scan
./lab.sh export
```

- **Syft / Grype:** ejecución real en contenedores, imágenes exportadas como archivo, sin Docker socket en un escáner.
- **Componentes legacy reales:** Django 3.2 y requests 2.31.0 en `/opt/legacy` de `records`; no son importados por el servicio activo. No se simula el descubrimiento de esos paquetes.
- **Expediente docente:** siete tarjetas curadas, rotuladas como caso; no se atribuyen a Grype. Las fallas locales no inventan IDs CVE.
- **Inteligencia:** snapshot real de FIRST EPSS y CISA KEV con fecha de consulta y origen. No se presenta EPSS como probabilidad de compromiso local.
- **Decisión:** índice ordinal `4 × L × max(impactos)` y tabla oficial **SSVC Deployer DT_DP v1.0.0**, conservada con licencia y procedencia. Las salidas de ambos modelos no se confunden.
- **Persistencia:** decisiones y reflexiones se guardan en SQLite, en un volumen del proyecto. La exportación incluye trazabilidad de IA y un hash del contenido.

## Aislamiento y alcance

Contiene fallas educativas intencionales. Ejecutar en el equipo de prácticas, **sin exposición a Internet**. Solo se publica la UI en `127.0.0.1`; los targets usan redes `internal: true`, sin privilegios generales ni socket Docker. Las sondas aceptan únicamente los tres nombres del caso. Todo dato y toda credencial de entrenamiento son sintéticos.

El escáner Grype tiene una red separada para actualizar su base. Ollama solo obtiene una red temporal durante la descarga del modelo; después se recrea con red interna. El plano de gestión accede a los targets para comprobarlos y aplicar las medidas del simulador; no es un diseño de producción ni un aislamiento frente a un administrador del host. [Arquitectura y modelo de amenaza](docs/ARQUITECTURA.md).

## Recursos, validación y continuidad

El caso base limita los cuatro servicios a **736 MiB combinados**; cada escáner corre por separado con límite de 1 GiB. Ollama suma un máximo de 4 GiB y se usa con targets pausados. Son límites configurados, no mediciones universales. Disco recomendado: **25 GB libres** como punto de partida; depende de arquitectura, imágenes y modelo.

```bash
./lab.sh test         # pruebas unitarias, incluidas las 72 ramas SSVC
./lab.sh smoke        # flujo real; deja evidencia de prueba y restablece targets
./lab.sh status
./lab.sh down        # conserva volúmenes y evidencia
```

[Validación de esta release](docs/VALIDACION.md) · [Solución de problemas](docs/SOLUCIONES.md) · [Plan docente](docs/DOCENCIA.md) · [Fuentes y licencias](NOTICE.md).

## Casos que inspiran las misiones

El fallo de inventario y verificación de parcheo se discute a partir de **Equifax**; la transferencia y exposición de datos, a partir del patrón de **MOVEit/CL0P**; la confianza en herramientas, a partir del incidente de **Trivy de marzo de 2026**. Son analogías documentadas: este repositorio no reproduce MOVEit, no atribuye sus CVEs a la aplicación del curso y no ejecuta herramientas comprometidas. [Hechos y adaptación](docs/CASOS_Y_FUENTES.md).

Código del curso: MIT, copyright 2026 Tomás Vera. La tabla SSVC y el software de terceros conservan sus propias licencias. No se incluyen pesos de modelos en Git. Empresas y condición OIV: **ficticias**. Mapeos ISO/MITRE/Chile: propuestas didácticas con evidencia, no equivalencias oficiales ni certificación.
