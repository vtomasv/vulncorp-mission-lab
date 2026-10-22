# Arquitectura de la campaña

```mermaid
flowchart LR
 B[Navegador del alumno] -->|loopback 8095| M[Plataforma y verificador]
 T[Terminal del alumno] -->|loopback 2222| M
 M -->|reenvío TCP fijo a SSH| W
 M -->|proxy fijo noVNC| W[Análisis · escritorio Linux]
 W -->|SSH 2222| O[Soporte]
 W -->|SSH 2222| A[Aplicaciones · Syft/Grype]
 W --> G[Gateway]
 O --> G
 O --> K[Copias]
 A --> G
 A --> R[Expedientes]
 G --> R
 M -->|lectura autenticada| E[Agentes y auditoría de servicios]
 M --> I[Ollama · Qwen3 en CPU]
```

## Segmentación efectiva

| Componente | Redes | Alcance esperado de los tres targets |
|---|---|---|
| Análisis | edge | gateway |
| Soporte | edge, support | gateway y backup |
| Aplicaciones | edge, app | gateway y records |
| Gateway | edge, app | entrada y dependencia de expedientes |
| Records | app | sin publicación al host |
| Backup | support | sin publicación al host |
| Plataforma | ui, edge, app, support, ai | plano de gestión de confianza |
| Ollama | ai | sin puerto publicado; red interna |

edge/app/support/ai son `internal:true`. Los puestos no tienen salida a Internet ni capacidades NET_ADMIN/NET_RAW. Dos interfaces en un puesto no lo convierten en router. La plataforma es el plano de gestión, con acceso deliberado a los servicios para verificarlos; no debe confundirse con una estación del estudiante.

La plataforma publica `127.0.0.1:8095` para web y `127.0.0.1:2222` para un reenvío TCP de destino fijo a workstation:2222. Docker no publica puertos de un contenedor conectado únicamente a redes internas; el reenvío permite mantener análisis solo en edge. SSH se autentica y cifra entre el cliente y sshd de análisis. noVNC reenvía HTTP/WebSocket únicamente a workstation:6080. No hay puertos publicados de soporte/aplicaciones, socket Docker, acceso privilegiado general ni selección arbitraria de destino en los proxies. La preparación de bases/modelos usa servicios distintos con egreso y retira la red temporal de Ollama.

## Quién puede acreditar qué

El usuario de práctica es **student, UID 1000**. El agente del puesto corre separado y admite acciones fijas mediante un socket Unix local: identidad, conectividad, inventario, escaneo, revisión, consulta y restricción. Los procesos de herramientas corren con UID 1000. No acepta rutas, hosts o comandos arbitrarios suministrados por el alumno.

Cada instalación genera secretos aleatorios en un volumen, legibles por el plano educativo y el agente, fuera del acceso de student. Los resultados de acciones se guardan en un diario privado y se firman HMAC. El endpoint remoto permite leer, no ejecutar. La identidad firmada enumera todas las interfaces del puesto; así se atribuyen correctamente solicitudes de una estación con dos redes.

Los targets registran solicitudes, IP de origen real, ruta, hora, estado HTTP y copia de la respuesta. El verificador acepta observaciones cuya IP corresponde a una interfaz verificada del puesto. Las pruebas del antiguo endpoint de gestión `/api/probe` conservan valor histórico, pero no acreditan estos objetivos.

El verificador filtra pruebas por inicio de campaña, aplica requisitos y concede cada premio una sola vez. SQLite conserva campañas, activaciones, observaciones y premios. Repetir una comprobación no duplica PX. Las observaciones auténticas hechas antes del desbloqueo pueden reutilizarse dentro de la misma campaña; no se finge que el alumno volvió a ejecutar algo.

## Llave de alumno y llaves privadas de la instalación

`training/ssh/vulncorp_student_ed25519` y su `.pub` forman un par compartido **intencionalmente público**. La interfaz ofrece ambas descargas mediante dos rutas exactas; no existe un servidor de archivos arbitrarios. Solo la llave pública se autoriza en sshd de análisis, desde un archivo de solo lectura fuera del hogar del alumno. El usuario es student; contraseña, acceso root y forwarding están deshabilitados.

La llave interna análisis → soporte/aplicaciones se genera por instalación y conserva su privada en el hogar de análisis. Las privadas de servidor y secretos HMAC permanecen en volúmenes privados. No son el par público del alumno ni se descargan desde la interfaz. La identidad HMAC del agente permite mostrar la llave pública y huella del servidor de análisis.

Ambos accesos ejecutan herramientas como UID 1000 en la misma red. El verificador acredita origen y resultados, no el protocolo de entrada. Compartir una llave de práctica no identifica personas: cada alumno necesita su propia instalación local.

## Alcance del inventario y de los controles

Aplicaciones contiene copias reales, de solo lectura, de `/opt/legacy` de records y del runtime de mission. Son **snapshots parciales**, no el filesystem completo ni un SBOM de toda la imagen. Los dos paquetes se instalan con versión y hash fijados y no son importados por el servicio activo. Syft genera CycloneDX; Grype recibe un SBOM recién generado por el agente, no un archivo editado por el alumno. Conserva aliases, descriptor de base, hashes y reporte completo.

La medida `restrict_export` cambia realmente la respuesta del gateway. No corrige la autorización en records ni instala una regla de firewall. El cierre exige 403 desde análisis y una transacción completada posterior al cambio, restricción vigente y residual que cite ambas pruebas.

## Memoria y límites

Límites configurados: plataforma 256 MiB; tres servicios 160 MiB cada uno; escritorio 512 MiB; soporte 128 MiB; aplicaciones 1280 MiB; Ollama 4 GiB. Total de servicios del juego con IA: **6752 MiB**, más sobrecarga del motor. Referencia: Docker con 8 GiB en host de 16 GB. Una herramienta pesada y una inferencia a la vez; el agente serializa acciones por puesto.

Los puestos arrancan con un proceso raíz y capacidades limitadas para preparar hogares, cambiar a UID 1000 y ejecutar sshd/X. Los tres puestos necesitan AUDIT_WRITE para abrir terminales SSH interactivas; está verificado explícitamente. El usuario interactivo carece de esas capacidades. El árbol de archivos del contenedor es de solo lectura, con hogares y directorios temporales específicos escribibles.

Esta es una frontera pedagógica local. El administrador del host Docker puede alterar contenedores, reloj, redes, secretos y base. HMAC protege procedencia frente al uso normal del puesto; no demuestra autoría individual ni resiste al propietario administrador. Cada estudiante necesita su propia instalación. No hay cuentas ni aislamiento multiusuario de producción.

## Rango de validación y continuación

La [continuación 4–6](CONTINUACION_4_6.md) agrega `validation` (128 MiB), `collector` (96 MiB) y ZAP bajo demanda (768 MiB), todos solo en la red interna `app`, sin puertos al host. Gateway sustituye el origen enviado por el alumno por el peer real y autentica el reenvío privado. El verificador relaciona ese origen con las direcciones de las estaciones firmadas. El nuevo volumen `range_state` conserva controles y registros por campaña; las estaciones no lo montan. Cambiar de campaña conserva el estado anterior para poder retomarlo.

Los endpoints de control y auditoría requieren una llave generada por instalación; el alumno usa comandos acotados del agente y no recibe esa llave. El marcador solo admite un programa fijo. El colector solo recibe el destino fijo desde la aplicación. No se aceptan comandos, rutas de archivo o URLs arbitrarias en esas acciones.

ZAP tiene una clave sintética pública de práctica y API solo interna. Se usa como proxy/análisis pasivo de cuatro solicitudes fijas. Sus alertas no sustituyen las pruebas de autorización; las referencias de progreso provienen además del agente y del target. El alumno puede explorar su instalación; el propietario de Docker puede modificar cualquier componente, por lo que el límite sigue siendo educativo y no un examen resistente al administrador.

## Segmento PHP y cuatro zonas finales

La red interna `php` conecta únicamente mission y los dos PHP. No hay puertos PHP publicados, Docker socket, red host ni agente con shell arbitraria. Ambos destinos usan UID 10001, raíz de archivos de solo lectura, 192 MiB, memoria de intercambio acotada y límites de procesos. Solo reciben una llave de runtime exclusiva, diferente de las llaves de firma de las estaciones.

Desde aplicaciones, un comando fijo viaja por el socket del agente a un endpoint autenticado de mission. El controlador elige una ruta PHP fija y conserva la respuesta HTTP con campaña, episodio, revisión, despliegue, secuencia y hash. El agente también firma un recibo de la acción. La interfaz puede leer evidencia y registrar razonamiento, pero no llamar al cambio operativo sin la llave interna. Un archivo modificado en el directorio del alumno no se convierte en prueba del servidor.

La ruta activa y los controles se persisten por campaña en SQLite. Los documentos y copias reales se guardan en un volumen separado, bajo el hash de la campaña. Un reinicio conserva copia y estado. Dos despliegues leen el mismo documento de esa campaña: el cambio de runtime no pierde datos. El controlador identifica los bloqueos propios como anteriores a PHP, separados de respuestas observadas del destino.

La reversión de ruta es una acción del guion; el retorno a la versión antigua y el 503 del documento son observaciones reales. El impacto de negocio y condición OIV siguen siendo antecedentes ficticios. La evidencia histórica conserva su valor documental y sus PX; los nuevos objetivos exigen comprobaciones de la revisión actual. No se reescribe la historia al reabrir un tratamiento.

`php-on` y `webscan-on` detienen el otro perfil para mantener respectivamente 7360 o 7744 MiB de límites con IA. Compose por sí solo permite al administrador forzar ambos: los lanzadores son la ruta soportada para el presupuesto de 8 GiB.
