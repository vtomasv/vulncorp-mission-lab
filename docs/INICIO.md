# Inicio para principiantes

## 1. Qué vas a construir

Una empresa ficticia con tres servicios: una entrada pública, un servicio de expedientes y un repositorio de copias. El centro de misión permite investigar, registrar evidencia y defender decisiones. No es una competencia de velocidad ni tiene notas intermedias.

**Imagen**: plantilla del software. **Contenedor**: instancia de una imagen en ejecución. **Puerto**: punto de escucha de un servicio. **Red**: qué servicios pueden comunicarse. **Volumen**: datos que sobreviven al contenedor. No necesitas memorizar comandos: sí explicar qué demuestra cada resultado.

## 2. Preparación del equipo

- 16 GB de RAM física; no necesitas GPU.
- Docker Engine con Compose v2, o Docker Desktop con contenedores Linux.
- En Windows: backend WSL2 de Docker Desktop. Sigue la instalación oficial antes de la clase; no hace falta que aprendas Linux por tu cuenta.
- Git y un navegador moderno.
- Referencia inicial: asignar 6-8 GB a Docker si el equipo lo permite, dos CPU para la inferencia y 25 GB libres de disco. Las imágenes y pesos se descargan la primera vez. El docente debe prepararlos antes de comenzar la jornada.
- Cierra solo las aplicaciones que tú decidas. El lanzador no detiene proyectos Docker ajenos.

Comprueba:

```bash
docker version
docker compose version
git --version
```

Debe aparecer una sección **Server** en Docker. Si ves solo Client, abre el motor y espera. `docker version` no es lo mismo que `docker --version`: el segundo solo confirma que existe el cliente.

## 3. Obtener e iniciar el caso

```bash
git clone https://github.com/vtomasv/vulncorp-mission-lab.git
cd vulncorp-mission-lab
```

macOS/Linux:

```bash
./lab.sh doctor
./lab.sh up
```

Windows PowerShell:

```powershell
.\lab.ps1 doctor
.\lab.ps1 up
```

Si PowerShell impide ejecutar scripts, una alternativa para **esta sesión** es:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\lab.ps1 up
```

No es necesario modificar una política permanente del equipo. Si tu organización administra esa política, utiliza los comandos Docker directamente o pide al docente el equipo de práctica:

```powershell
docker compose build mission records
docker compose up -d --wait mission records gateway backup
```

Espera la construcción. Debes ver cuatro servicios iniciados, sin fallos de healthcheck. Abre **http://localhost:8095** y selecciona un cliente.

## 4. Tu primera evidencia

1. En **Mapa operativo**, pulsa **Probar función de negocio**.
2. Debe aparecer `status: completed` y `transaction_id: TRAIN-...`.
3. Pulsa **Probar exportación**. Al inicio devuelve HTTP 200 con registros que dicen PERSONA FICTICIA.
4. Abre **Evidencias**. Comprueba dos observaciones distintas, con hora, origen, zona y hash.
5. En **Misiones → Clase 1**, explica qué demuestra cada una. Una transacción exitosa no demuestra que sea segura.

## 5. Conocer la terminal sin perderse

Abre la terminal en la carpeta que contiene `compose.yaml`. Cada comando del lanzador opera ese proyecto.

| Acción | macOS/Linux | Windows |
|---|---|---|
| Ver el estado | `./lab.sh status` | `.\lab.ps1 status` |
| Ver rutas públicas | `./lab.sh discover public` | `.\lab.ps1 discover public` |
| Probar función | `./lab.sh probe public transaction` | `.\lab.ps1 probe public transaction` |
| Detener sin borrar evidencia | `./lab.sh down` | `.\lab.ps1 down` |

`Ctrl+C` detiene el comando que estás viendo, no necesariamente los contenedores que ya están en segundo plano. `up -d` significa iniciar en segundo plano. `down` retira contenedores y redes de este proyecto; conserva los volúmenes. No uses `down -v` si quieres conservar tus decisiones y los pesos del modelo.

## 6. Conservar el aprendizaje

- Las reflexiones y decisiones del centro de misión viven en un volumen SQLite.
- **Exportar evidencia** descarga un JSON de tu expediente.
- El lanzador `export` lo guarda también en `artifacts/expediente.json`.
- Syft y Grype escriben reportes en `artifacts/`. Esos archivos no se suben a Git.
- Si quieres entregar los comandos ejecutados en terminal, conserva sus salidas junto al expediente. No se incluyen automáticamente en la exportación de la UI.

Continúa con [Clase 1](../labs/01-superficie/ESTUDIANTE.md). Si aparece un problema, consulta [Soluciones](SOLUCIONES.md).
