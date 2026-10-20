# Instructor · Clase 3

[Guía y agenda](ESTUDIANTE.md). Descargar pesos previamente con `ai-prepare`. Usar Qwen3 1.7B y CPU; no convertir la jornada en una comparación de modelos grandes.

## Ejemplo trabajado

F-02 para NubeAndes: L=4; impactos operación=5, personas=2, datos=5, finanzas=5. Máximo I=5 → índice 80. Para agua, el mismo hallazgo usa I=2 → índice 32. El CVSS 7.5 docente no cambia.

F-03 para agua: L=3; máximo I=5 → 60. La recuperación importa más que la API administrativa. El giro puede aumentar la preocupación sobre una copia única; exigir nueva evaluación, no imponer un valor como verdad automática.

No existe una salida SSVC derivada únicamente de esas cifras. Pedir sus cuatro entradas y premisas. En la tabla oficial, Active/Open/Yes/High produce Immediate; Active/Open/Yes/Low produce Out-of-Cycle. **Active no se justifica con un probe de entrenamiento ni con EPSS alto.**

## Cartera

Con las premisas iniciales, ejemplos defendibles son A+B para salud, B+C para agua y A+C para digital. Son ejemplos; una alternativa con evidencia puede ser mejor. El motor solo comprueba presupuesto y ventana, no corrección de la estrategia.

No sumar los índices ordinales como dinero ni asegurar que cerrar dos CVEs representa una reducción proporcional de riesgo. Preguntar qué ruta y qué servicio quedan protegidos, qué se posterga y quién acepta el residual.

## IA: demostración de capacidad y crítica

1. Conservar evidencia antes de pausar targets.
2. `ai-on` inicia el modelo aislado y pausa targets. El centro de misión mantiene SQLite y corpus.
3. Enviar una consulta corta con un hallazgo y el cliente.
4. Mostrar digest del modelo y fuentes recuperadas.
5. Verificar una afirmación, incluso si el ID citado existe.
6. Guardar revisión humana. El validador no es un verificador semántico.

Comparar cinco minutos de razonamiento manual con el tiempo de inferencia **más revisión**. Una salida larga no significa más valor. Si no hay modelo operativo, usar el ejemplo sintético rotulado para crítica y repetir inferencia cuando la infraestructura esté disponible.

## Comprobar tratamiento

Después de `ai-off`, targets arrancan iniciales. Aplicar restricción de exportación desde el panel, repetir export (403) y transaction (200/completed). Pedir al auditor que verifique que un 503 por dependencia apagada no se presente como control efectivo.

La mitigación retira una ruta pública; records sigue sin autorización. No presentar esto como corrección de raíz. La rotación de llave modifica acceso al catálogo, no prueba una recuperación.

## Quince minutos del comité: controles con evidencia

Usar el paso 13 para exigir dos relaciones argumentadas entre conducta, medida, MITRE, ISO y deber OIV simulado. No aceptar una colección de IDs sin condiciones. La contraprueba buscada es rechazar «diagnóstico 403 demuestra M1030/A.8.22»: se restringió una ruta HTTP; las redes no cambiaron. También rechazar «catálogo 200 demuestra continuidad». El registro del cambio y sus pruebas puede discutir el art. 8 b), sin acreditar por sí solo el conjunto de obligaciones. Guardar el razonamiento en reflexión 3-4 y conservar tabla aparte.

## Últimos 30 minutos

Cada persona explica la decisión más difícil, una salida de IA corregida o rechazada y una pregunta que cambia la prioridad. Exportar. Sin nota ni ranking.
