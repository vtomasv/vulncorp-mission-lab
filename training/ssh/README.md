# Llaves PÚBLICAS de entrenamiento

Este par Ed25519 es **intencionalmente público**, incluida su llave privada, para entrar como alumno en la instalación local de VulnCorp. No es una credencial real ni un secreto del proyecto.

| Dato | Valor |
|---|---|
| Usuario | `student` |
| Contraseña de cuenta SSH | No se usa; autenticación por contraseña deshabilitada. |
| Frase de paso de esta llave | Vacía; no se solicita. |
| Llave privada de práctica | [vulncorp_student_ed25519](vulncorp_student_ed25519) |
| Llave pública autorizada | [vulncorp_student_ed25519.pub](vulncorp_student_ed25519.pub) |
| Destino por defecto | `127.0.0.1:2222`, puesto de análisis |

Desde la raíz del repositorio ejecuta `./lab.sh ssh` o `.\lab.ps1 ssh`. El lanzador prepara los permisos de una copia local y verifica la llave pública del servidor de tu propio contenedor. También puedes descargar el par desde **Conectar por SSH** en la plataforma y configurar tu cliente siguiendo [la guía SSH](../../docs/SSH.md).

Esta llave solo se autoriza en el puesto de análisis. Soporte y aplicaciones usan otra llave generada por instalación y solo se alcanzan desde dentro del laboratorio. Los secretos HMAC, las llaves privadas de servidor y la llave privada interna entre puestos **no se publican**.

Usa este par exclusivamente en la práctica local. Al estar publicado, no identifica a una persona ni protege un servidor real o un despliegue compartido.
