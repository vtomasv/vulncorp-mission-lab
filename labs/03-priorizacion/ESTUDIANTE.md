# Continuidad · decide y demuestra el efecto

## 11. Dos dueños, un hallazgo

En la ruta lee primero salud y luego agua. Evalúa F-02 para ambos: conserva el hecho técnico y L, reconsidera las cuatro consecuencias y vincula una prueba de exportación real.

El índice es `4 × L × máximo(operación, personas, datos, finanzas)`. Cada nivel está entre 1 y 5; es ordinal, no porcentaje. Compara, por ejemplo, L=4 con impacto máximo 4 y luego 2: obtienes 64 y 32. Esos valores ilustran el cálculo; tus premisas deben explicarse al dueño.

Selecciona las cuatro entradas del árbol SSVC Deployer. Su Human Impact tiene una definición propia: no copies el impacto máximo de la fórmula. No atribuyas explotación real a una CVE por haberla reproducido en el laboratorio.

## 12. Una segunda mirada

Desde análisis, entra a aplicaciones si hace falta:

```bash
ssh appdesk
lab ia
```

Espera la inferencia real de Qwen3 local en CPU. Vuelve al objetivo de la ruta: contrasta una afirmación completa con su fragmento, no solo con la existencia del ID. Registra aceptar, corregir o rechazar, citando la frase y tu fundamento. El modelo no ejecuta cambios, calcula el riesgo ni acepta el residual.

## 13. Cuatro horas para proteger

En la ruta selecciona una cartera de hasta 4 h y 15 min de ventana. Incluye la restricción de exportación A para la prueba posterior. Explica qué pospones y por qué. Relaciona hipótesis de conducta, objetivo de control y deber de gestión de la OIV ficticia con MITRE, ISO y ley; delimita lo que esa relación no prueba.

Restringir `/api/export` no acredita segregación de redes ni cumplimiento integral. La calidad del fundamento se discute con el dueño, aunque el presupuesto sea válido.

## 14. Una medida en la empresa

En aplicaciones:

```bash
lab proteger
```

El comando pide tu motivo. Escribe al menos 30 caracteres que expliquen propósito y comprobaciones posteriores, y pulsa Enter. El gateway debe confirmar. La causa raíz de autorización en records sigue pendiente.

## 15. Proteger sin interrumpir

Vuelve desde aplicaciones a análisis:

```bash
exit
curl -s -o /tmp/exportacion.json -w '%{http_code}\n' http://gateway:8080/api/export
curl -s http://gateway:8080/api/transaction | jq
```

Debes observar **403** y **completed**, ambos después de aplicar la medida. Un 503 no acredita continuidad. En la ruta registra el residual y cita las dos pruebas posteriores. La plataforma comprueba también que la restricción siga activa.

## Defensa del equipo

Presenta la decisión antes/después, el dueño responsable, el alcance del control y las condiciones de aceptación. Un equipo auditor cuestiona una afirmación legal, una técnica y una de la IA. Formula el siguiente trabajo pendiente para corregir la causa raíz y verificar recuperación real en una ampliación del juego.
