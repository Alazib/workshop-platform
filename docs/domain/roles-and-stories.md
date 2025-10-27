# Roles y Historias de Usuario — Borrador inicial

## Roles
- **admin**
  - Permisos: gestionar la plataforma, crear/eliminar organizadores, ver métricas y facturación, configuración de pasarelas de pago.
- **organizer**
  - Permisos: crear/editar sus talleres, definir precio y cupo, ver lista de inscritos para sus talleres, exportar inscritos CSV.
- **attendee**
  - Permisos: navegar talleres, inscribirse, pagar, cancelar según política, ver su historial.
- **accountant** (opcional)
  - Permisos: ver reportes financieros y exportes, acceso read-only a pagos.

## Historias de usuario principales
1. Como **organizer**, quiero **crear** un taller (título, descripción, fecha, hora, cupo, precio) para ofrecerlo al público.  
2. Como **attendee**, quiero **inscribirme** en un taller y **pagar** (Stripe / PayPal / Bizum / transferencia) para asegurar mi plaza.  
3. Como **organizer**, quiero **ver la lista de inscritos** y exportarla a CSV.  
4. Como **attendee**, quiero **recibir un email de confirmación** y un recordatorio 24h antes del taller.  
5. Como **admin**, quiero **ver métricas de ventas** y facturación por mes y descargar reportes.  
6. Como **attendee**, quiero **anular mi inscripción** dentro de la política de cancelación y (si aplica) solicitar reembolso.  
7. Como **organizer**, quiero **definir descuentos o códigos promocionales** para mis talleres.  
8. (Opcional) Como **attendee**, quiero apuntarme a una **lista de espera** si un taller está lleno.

## Reglas de negocio iniciales (propuesta)
- Solo `organizer` y `admin` pueden crear talleres; `organizer` gestiona sólo sus talleres.  
- Pago y confirmación:
  - Cuando la inscripción incluye pago, la plaza queda **reservada** solo tras confirmación del pago (estado: pending → paid → confirmed).  
  - Para transferencias bancarias, el estado será `pending` hasta verificación manual (o webhook de banco), con caducidad (ej.: 72h).  
- Cancelaciones:
  - Política por defecto: cancelación gratuita hasta 48h antes; reembolso según política del organizer.  
- Pagos:
  - Permitimos integración con Stripe, PayPal, Bizum y pago por transferencia.  
  - `admin` configura credenciales para cada pasarela; `organizer` gestiona precios pero no credenciales.
