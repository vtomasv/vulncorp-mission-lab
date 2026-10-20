# VulnCorp · campaña de gestión de vulnerabilidades

## La experiencia que se construye

Un laboratorio individual y extensible, con un tablero de objetivos, puestos de trabajo reales en Docker y una campaña de quince desafíos. La interfaz del jugador no usa clases ni horarios académicos. Muestra una zona, un objetivo activo, instrucciones progresivas y un acceso al escritorio. El cuaderno y las herramientas aparecen en contexto.

El ciclo es **leer el encargo → predecir → entrar al puesto → ejecutar → contrastar la comprobación → explicar → avanzar**. La plataforma comprueba resultados observables; no entrega puntos por pulsar «he terminado». Los puntos reconocen hitos de práctica y no afectan la nota del curso. No hay clasificación por velocidad ni penalización por reintentar.

## Campaña inicial

| Zona | Desafío | Evidencia o criterio comprobable |
|---|---|---|
| 1. Terreno | Primer contacto | Comando ejecutado en el puesto de análisis; identidad y zona reales. |
| | El servicio sigue vivo | Transacción completada desde el puesto, registrada por el servicio. |
| | El límite de la red | Resolución y conectividad comprobadas desde el puesto público. |
| | La puerta inesperada | Exportación y diagnóstico observados desde esa zona. |
| | Otro punto de vista | Acceso SSH a soporte y observación desde su red. |
| 2. Señales | Inventario con procedencia | Syft sobre una copia de archivos real y de solo lectura, con alcance explícito. |
| | Una alerta no es una decisión | Grype real, base fechada, identificadores y alias conservados. |
| | Presente y utilizado | Revisión de código real y presencia del componente, sin afirmar explotación. |
| | Dos errores del proveedor | Comparación de inventarios y clasificación razonada de duplicado/atribución. |
| | Un expediente defendible | Referencias reales y clasificaciones con límites registrados. |
| 3. Continuidad | Dos dueños, un hallazgo | Evaluaciones de dos clientes; cálculo determinista y contexto explícito. |
| | Una segunda mirada | Inferencia real local, fuentes y revisión humana vinculada. |
| | Cuatro horas para proteger | Cartera dentro del presupuesto, control y alcance argumentados. |
| | Una medida en la empresa | Cambio ejecutado desde el puesto y confirmado por el servicio. |
| | Proteger sin interrumpir | Exportación denegada y transacción completada después del cambio; residual documentado. |

La implementación conserva el progreso con registros de comprobación e identificadores únicos: repetir una prueba no multiplica puntos. Cada desafío se desbloquea con sus requisitos. Un reinicio no convierte una observación histórica en un estado actual.

## Puestos y redes

- **Análisis:** escritorio Linux ligero accesible por noVNC o SSH desde la terminal del alumno; ambos entran al mismo puesto, que solo ve la zona pública del caso.
- **Soporte:** estación SSH interna con acceso a las copias. Se alcanza desde el puesto de análisis; no publica SSH al host.
- **Aplicaciones:** otra estación SSH con acceso a la aplicación y a archivos de inventario de solo lectura; ejecuta Syft y Grype sin socket Docker.
- **Servicios:** entrada pública simulada, aplicación y copias mantienen redes separadas. Los puestos no actúan como routers.
- **Plano educativo:** comprueba resultados y guarda el expediente. La plataforma publica web y SSH solo en loopback. noVNC y SSH se entregan mediante reenvíos de destino fijo al escritorio; no hay un proxy abierto a otros destinos.

Los puestos no tienen egreso a Internet durante el juego. Las descargas de imágenes, bases y modelos corresponden a la preparación. El host Docker sigue bajo control de su propietario: esta edición local no es un sistema de examen resistente a un administrador malicioso ni un despliegue multiusuario de producción.

## Verificación y criterio

Se distinguen dos tipos de hitos:

1. **Técnicos:** resultado de red, componente encontrado, herramienta ejecutada o cambio confirmado. Se comprueban con registros de los servicios y un agente del puesto separado del usuario de práctica.
2. **De decisión:** cálculos, referencias, presupuesto y revisión humana registrados. La plataforma comprueba estructura, relaciones y restricciones; la calidad de la argumentación se contrasta en la discusión docente.

Un texto escrito, un JSON cargado por el usuario o un código HTTP aislado no bastan para completar la campaña. Los premios no equivalen a certificación de competencia ni acreditan cumplimiento legal.

## Uso docente de las tres jornadas

La zona 1 ocupa la primera jornada; la zona 2, la segunda; la zona 3, la tercera. Cada una ocupa 420 minutos de reloj: 20 de predicción, 35 de conceptos, 25 de demostración, dos bloques de 100 de juego y contraste, 70 de discusión, 30 de reflexión y 40 de pausas distribuidas. Se rota entre analista, dueño y auditor. Las sesiones se organizan desde fuera del juego.

La duración no se llena con esperas artificiales: se amplía mediante hipótesis, pruebas negativas, entrevistas, contrapruebas y defensa de decisiones. El único examen calificable sigue siendo el final del curso.

## Extensión

Nuevas zonas se agregan al catálogo de campaña con ID, requisitos, puntos, instrucciones, pistas y función de comprobación. El núcleo no debe asumir que hay tres clases o tres zonas. Cada nuevo objetivo exige especificar qué prueba lo acredita y qué no permite concluir. Los nuevos servicios se añaden con su propia segmentación y presupuesto de recursos.
