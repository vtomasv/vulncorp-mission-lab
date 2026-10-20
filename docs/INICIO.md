# Tu primera entrada a VulnCorp

## Preparar una vez

Necesitas 16 GB de RAM física, Docker Engine/Desktop con contenedores Linux, Compose **2.24.4+**, Git y navegador. Asigna **8 GB a Docker**; deja 30 GB libres para imágenes, escritorio, base de Grype y modelo. Sin GPU. En Windows usa Docker Desktop con WSL2.

Abre una terminal en la carpeta donde guardarás el proyecto:

```bash
git clone https://github.com/vtomasv/vulncorp-mission-lab.git
cd vulncorp-mission-lab
```

macOS/Linux:

```bash
./lab.sh doctor
./lab.sh prepare-game
```

Windows PowerShell:

```powershell
.\lab.ps1 doctor
.\lab.ps1 prepare-game
```

Espera a que termine. La preparación construye los puestos, descarga la base de Grype, permite su lectura desde aplicaciones y descarga Qwen3. La conexión temporal de descarga del modelo se retira al finalizar. No se descarga contenido desde los puestos durante el juego.

Si PowerShell bloquea scripts, consulta la política del equipo con el docente. Para una sesión personal puedes usar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`; no hace falta un cambio permanente. El lanzador de Windows todavía requiere validación en una máquina Windows.

## Jugar

1. Abre [localhost:8095](http://localhost:8095).
2. Lee **Primer contacto**. Puedes pulsar **Entrar al puesto** para noVNC o **Conectar por SSH** para ver usuario, llaves y comandos. El usuario es `student` y no se usa contraseña. En el diálogo SSH, **Usar mi terminal y ver los pasos** muestra las instrucciones junto al objetivo sin abrir el escritorio.
3. En noVNC, haz clic dentro de la terminal Linux y pulsa **Pegar en el puesto**. Para usar tu terminal ejecuta `./lab.sh ssh` o `.\lab.ps1 ssh` en la carpeta del proyecto y escribe `lab iniciar` una vez conectado.
4. Revisa el comando y pulsa **Enter**. Verás `uid=1000(student)`, el nombre del puesto y un ID de evidencia.
5. En unos segundos aparece **Objetivo comprobado · +40 PX**. Continúa al siguiente objetivo.

Los pasos se muestran de uno en uno. «Siguiente paso» cambia la instrucción; no acredita el objetivo. «Necesito una pista» ofrece ayuda sin penalización. «Volver a la ruta» conserva el escritorio abierto y tu trabajo.

El botón de pegar solo escribe una línea; no la ejecuta. Si un comando queda escrito dos veces, limpia la línea con Ctrl+U antes de pegar. Si necesitas interrumpir un comando usa Ctrl+C. Para abrir otra terminal puedes pulsar Ctrl+Alt+T dentro del escritorio.

## Moverse entre puestos

En análisis, `ssh ops` entra a soporte y `ssh appdesk` a aplicaciones. El prompt cambia. `exit` vuelve al puesto anterior. No entres a aplicaciones desde soporte: vuelve primero a análisis. Si ejecutas un comando en la perspectiva incorrecta, puede no haber evidencia válida; revisa la ubicación que indica la guía.

Estos son computadores Linux en contenedores distintos. noVNC y tu cliente SSH acceden al mismo puesto de análisis. Soporte y aplicaciones siguen siendo internos. El [par de llaves de práctica](../training/ssh/README.md) es intencionalmente público y está disponible en la interfaz; la [guía SSH](SSH.md) explica permisos, huellas y conexión manual.

## Guardar y volver

El cuaderno muestra objetivos acreditados, decisiones y procedencia. **Exportar expediente** descarga JSON con el historial y un hash. La base SQLite, hogares de los puestos, base de Grype y pesos viven en volúmenes Docker.

| Acción desde la carpeta del proyecto | macOS/Linux | Windows |
|---|---|---|
| Volver a iniciar | `./lab.sh up` | `.\lab.ps1 up` |
| Entrar desde tu terminal | `./lab.sh ssh` | `.\lab.ps1 ssh` |
| Ver estado | `./lab.sh status` | `.\lab.ps1 status` |
| Detener sin borrar | `./lab.sh down` | `.\lab.ps1 down` |
| Exportar a artifacts | `./lab.sh export` | `.\lab.ps1 export` |
| Liberar RAM de IA | `./lab.sh ai-off` | `.\lab.ps1 ai-off` |
| Encender IA | `./lab.sh ai-on` | `.\lab.ps1 ai-on` |

Apagar IA conserva puestos y medidas. Reiniciar los servicios vulnerables devuelve sus fallas iniciales: sus controles son volátiles. El expediente histórico se conserva; una evidencia pasada no garantiza estado actual. No uses `down -v` para una pausa: elimina los volúmenes del proyecto.

Continúa con [Terreno](../labs/01-superficie/ESTUDIANTE.md). Ante un problema consulta [Soluciones](SOLUCIONES.md).
