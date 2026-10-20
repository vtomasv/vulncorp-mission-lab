# Clase 3 · La prioridad cambia de dueño

**Duración:** 7 horas efectivas. **Evaluación:** formativa, sin nota. **Requisitos:** expediente y observaciones de clases 1-2. La IA se prepara antes de la jornada para no consumirla descargando pesos.

## La decisión de las 08:10

Cuatro horas de ingeniería. Quince minutos de ventana. Mismos componentes y hallazgos, tres clientes con misiones distintas. No puedes resolver el encargo diciendo «primero todo lo crítico».

## Agenda

| Min | Actividad |
|---:|---|
| 20 | Recuperar una afirmación técnica y una consecuencia de negocio. |
| 40 | CVSS, EPSS, KEV; índice ordinal; SSVC Deployer; urgencia y viabilidad. |
| 30 | Ejemplo completo con dueño, cálculo, árbol y evidencia. |
| 110 | Laboratorio A: decidir para el primer cliente. |
| 110 | Laboratorio B: cambiar de cliente y auditar IA local. |
| 80 | Cartera, giro de negocio y mitigación verificada. |
| 30 | Reflexión, revisión individual y exportación. |

## Laboratorio A · Construir una decisión defendible

### Paso 1. Separa cuatro señales

- **CVSS:** severidad técnica. Conserva versión y vector.
- **EPSS:** predicción global de explotación de una CVE en 30 días; el percentil es su posición relativa. No es probabilidad de compromiso del cliente.
- **KEV:** explotación conocida; no prueba compromiso de tu activo. Ausencia no implica seguridad.
- **Contexto:** función, acceso, condiciones, controles probados y consecuencias acordadas con el dueño.

En Hallazgos se muestran valores EPSS reales del snapshot y su fecha. Los hallazgos locales sin CVE no reciben un EPSS inventado.

### Paso 2. Habla con el dueño

Selecciona un cliente, lee su misión, RTO/RPO y tarjetas. Anota las consecuencias en cuatro dimensiones: **operación, personas, datos y finanzas**. Usa niveles de 1 a 5 y explica las anclas del caso:

1. Menor, sin degradación relevante.
2. Local, con alternativa suficiente.
3. Degradación relevante o exposición acotada.
4. Supera una tolerancia, afecta datos sensibles o múltiples clientes.
5. Función esencial sin alternativa suficiente o consecuencias máximas según el BIA del cliente.

Estos umbrales son pedagógicos: no son una escala legal ni un estándar universal. Usa las tarjetas para defenderlos; si falta un dato, regístralo.

### Paso 3. Calcula el índice

En **Decisiones → Evaluar**, selecciona L de 1 a 5 y cuatro impactos. El motor calcula:

```text
I = máximo(operación, personas, datos, finanzas)
R = 4 × L × I
```

L describe plausibilidad contextual: 1 sin ruta identificada tras pruebas acotadas; 2 ruta indirecta con condiciones; 3 ruta plausible o probada parcialmente; 4 ruta reproducida en el caso; 5 evidencia de explotación del activo. No se obtiene convirtiendo EPSS a un nivel.

Ejemplo sintético: L=4 e I=5 → 80. Ese 80 **no es 80%**. Si la evidencia de un control permite justificar L=2, el residual sería 40, conservando I=5. No reduzcas L por declarar un firewall: comprueba el control.

### Paso 4. Recorre SSVC sin mezclar modelos

Usamos **SSVC Deployer Patch Application Priority DT_DP v1.0.0**, de CERT/CC. El JSON oficial está en `data/ssvc/deployer.json`; sus 72 combinaciones se comprueban con tests.

Entradas: estado de explotación, exposición del sistema, automatización e **impacto humano**. Salidas: Defer, Scheduled, Out-of-Cycle e Immediate. No son las etiquetas Track/Track*/Attend/Act de CISA Coordinator.

El impacto humano combina **misión y seguridad** con su definición oficial. No se convierte automáticamente del I máximo del índice. Lee la ayuda del formulario y [la documentación del desplegador](https://certcc.github.io/SSVC/howto/deployer_tree/).

Una prueba exitosa en un target de entrenamiento no acredita explotación activa en el mundo real. No selecciones `Active` solo porque hiciste un `probe` o porque EPSS sea alto. La categoría Public PoC también incluye métodos de explotación bien conocidos según su definición.

### Paso 5. Guarda F-01 a F-04

Para cada uno registra responsable, estado inherente, evidencia/ contexto y una justificación que conecte consecuencia y decisión. Los IDs `EV-*` son documentos de contexto o hipótesis; los IDs de pruebas ejecutadas aparecen como observados. No los trates como intercambiables.

El sistema conserva cada evaluación; reevaluar no borra las anteriores. El índice ayuda a comparar dentro de una política; no puede desplazar por sí solo un tratamiento que requiere urgencia mayor.

## Laboratorio B · Otro dueño y una segunda mirada

### Paso 6. Cambia el cliente

Evalúa de nuevo F-02 y F-03 para otro cliente. No modifiques CVSS ni la evidencia técnica porque cambió el dueño. Abre la comparación.

Referencia trabajada del índice, disponible después de justificar:

| Hallazgo | Salud | Agua | Servicios digitales |
|---|---:|---:|---:|
| F-01, L=1 | 8 | 4 | 8 |
| F-02, L=4 | 64 | 32 | 80 |
| F-03, L=3 | 60 | 60 | 24 |
| F-04, L=3 | 36 | 48 | 48 |

Son valores sintéticos de referencia, no una respuesta única calificable. Debes justificar por qué asignas impacto y cómo se relaciona con SSVC. Otras decisiones requieren evidencia y límites claros.

### Paso 7. Activa IA local

Primera preparación, con Internet:

```bash
./lab.sh ai-prepare
```

Durante la clase:

```bash
./lab.sh ai-on
```

Windows: `.\lab.ps1 ai-prepare` y `.\lab.ps1 ai-on`. Se pausan targets; permanecen centro de misión y evidencia. Ollama usa CPU, un modelo Qwen3 1.7B y límite de 4 GB. No hay un endpoint de IA publicado al host.

Abre **IA local**. Debe decir **LISTO · CPU** y mostrar el modelo. Si dice apagado o sin modelo, no se ha realizado inferencia. Hay un ejemplo sintético para crítica expresamente rotulado; no debe presentarse como respuesta real.

### Paso 8. Pide contexto, no una autorización automática

Consulta F-02: «¿Qué debo preguntar al dueño antes de priorizar? Separa hechos, hipótesis y datos faltantes. Propón dos tratamientos y cita las fuentes recibidas».

Espera la inferencia real. El panel guarda modelo, digest, versión del prompt, fuentes recuperadas, salida, tiempo y errores de referencias. La CPU puede tardar; no se promete una latencia universal.

Verifica **una afirmación completa**: ID citado → texto recuperado → dato del caso → conclusión. Que el ID exista no prueba que el fragmento sustente lo dicho. El asistente no observa una prueba solo por haber leído su descripción.

Registra aceptar, corregir o rechazar **con una razón**. Una recomendación fluida sin sustento no es competente. No se permite aceptar una salida con referencias que el validador detectó como inválidas.

### Paso 9. Vuelve a los targets

```bash
./lab.sh ai-off
```

Libera la RAM del modelo y reinicia el escenario. Repite una prueba antes de aplicar medidas: los controles de los targets son efímeros y la bitácora es histórica.

## Comité · Elegir y demostrar

### Paso 10. Diseña una cartera

En Decisiones, selecciona paquetes. Presupuesto sintético: 4 horas de ingeniería y 15 minutos de interrupción acumulada.

| Paquete | Ingeniería | Interrupción |
|---|---:|---:|
| A · Restringir exportación | 2 h | 0 min |
| B · Rotar llave de copias | 2 h | 10 min |
| C · Restringir diagnóstico | 1 h | 5 min |
| D · Actualizar legacy | 3 h | 30 min |

El sistema rechaza combinaciones que exceden el caso. **La cartera es planificación:** no ejecuta automáticamente todos los paquetes. Las medidas A/B/C se pueden aplicar individualmente en el simulador. D es una opción de negociación que queda fuera de la ventana, no una actualización implementada en estas clases.

### Paso 11. Recibe el giro y revisa

Pulsa **Revelar giro de misión** en el mapa. Lee el nuevo hecho y explica qué entrada de tu evaluación cambia y cuál permanece. Conserva la decisión previa. Una excepción no se vuelve permanente por haber sido aceptada una vez.

### Paso 12. Aplica A y comprueba dos resultados

En Decisiones, pulsa **Aplicar con justificación** en Restringir exportación. Describe el motivo y las pruebas esperadas. Después ejecuta:

```bash
./lab.sh probe public export
./lab.sh probe public transaction
```

Resultado esperado: export HTTP **403** y transacción HTTP **200**, `completed`. Repite con los botones para guardar evidencia.

El gateway limita la ruta pública; records sigue sin implementar autorización. Esto es una **mitigación temporal**. La causa raíz no está corregida, la biblioteca no se actualizó y no se probó ausencia de compromiso. Reevalúa el residual solamente con lo que la prueba demuestra.

Puedes aplicar B y comprobar que la llave antigua deja de abrir el catálogo; no declares restauración probada: estas clases no implementan restauración ni borrado de copias.

## Entrega formativa

Exporta expediente y reportes. Deben quedar: dos clientes comparados, cuatro decisiones iniciales, una revisión de IA real o crítica sintética claramente identificada si hubo un fallo, una cartera, una reevaluación y dos pruebas después de una medida.

**Éxito observable:** puedes explicar la diferencia entre severidad, índice y urgencia; el dueño cambia una premisa; la IA tiene revisión humana; la medida reduce una exposición y preserva una función.
