# Roles y Historias de Usuario — Versión 4 (multi-admin + CRM de asistentes)

## Roles
| Rol | Descripción | Permisos clave |
|------|--------------|----------------|
| **admin** | Usuario con privilegios de administración completa. Puede haber varios administradores. Se encargan de crear talleres, gestionar usuarios, asignar organizadores, administrar pagos y acceder a reportes. | Crear/editar talleres, categorías y usuarios; asignar organizadores; confirmar pagos; gestionar políticas; enviar comunicaciones a attendees; ver métricas globales. |
| **organizer** | Persona que imparte uno o varios talleres. No puede crear ni editar talleres, solo consultar los que tiene asignados y sus inscritos. | Consultar talleres asignados, ver inscritos, estadísticas, descargar listas. |
| **attendee** | Usuario participante que se inscribe y paga para asistir a talleres. Sus datos de contacto (nombre, email, teléfono) se almacenan en la base de datos de asistentes. | Ver talleres, inscribirse, pagar, cancelar dentro del plazo legal, recibir recordatorios e información si ha dado su consentimiento. |
| **accountant (opcional)** | Usuario de solo lectura para supervisar reportes financieros. | Ver informes y exportes financieros. |

---

## Historias de usuario principales
1. Como **admin**, quiero **crear talleres** y asignar uno o varios organizadores a cada uno.  
2. Como **admin**, quiero **gestionar varios administradores**, pudiendo crear o eliminar cuentas de otros admins.  
3. Como **admin**, quiero **gestionar pagos**, validar transferencias manuales y configurar pasarelas de pago (Stripe, PayPal, Bizum).  
4. Como **admin**, quiero **consultar la base de datos de attendees** (nombre, email, teléfono) y **enviarles información** sobre futuros talleres si han aceptado recibirla.  
5. Como **organizer**, quiero **ver los talleres que imparto**, sus sesiones, inscritos y estadísticas.  
6. Como **attendee**, quiero **inscribirme** y **pagar** mi plaza (Stripe / PayPal / Bizum / transferencia).  
7. Como **attendee**, quiero **recibir confirmación automática** del pago y recordatorios antes de cada sesión.  
8. Como **attendee**, quiero **cancelar mi inscripción** dentro del plazo legal y recibir reembolso.  
9. Como **admin**, quiero **ver estadísticas globales** (asistencia, ingresos, talleres, usuarios).  
10. Como **organizer**, quiero **ver estadísticas de asistencia** de los talleres que imparto.  

---

## Reglas de negocio consolidadas
- Puede haber **varios administradores** con iguales permisos de gestión.  
- Solo los administradores pueden crear, modificar o eliminar talleres, categorías y usuarios.  
- Los organizadores solo pueden visualizar talleres asignados.  
- Un taller puede tener **uno o varios organizadores**.  
- Los talleres pueden pertenecer a **una categoría** y tener **múltiples sesiones/fechas**.  
- Todos los cobros se procesan a través de las cuentas del **admin**, no de los organizadores.  
- Política de cancelación **global**, conforme a la legislación española/europea.  
- Tipos de pago:
  - **Automáticos:** Stripe, PayPal, Bizum → confirmación por webhook.  
  - **Manual:** Transferencia → validación manual por el admin.  
- Estados de inscripción:
  - `pending` → pago iniciado  
  - `paid` → pago recibido  
  - `confirmed` → plaza asegurada  
  - `cancelled` → cancelación o pago expirado  
- Base de datos de asistentes:
  - Al inscribirse, los asistentes pueden aceptar recibir información sobre futuros talleres.  
  - Los datos almacenados incluyen: nombre, email, teléfono, consentimiento de contacto.  

---

## Futuras ampliaciones previstas
- Sistema de lista de espera.  
- Envíos masivos y segmentados (newsletter interna).  
- Consentimiento RGPD y opción de baja (“opt-out”).  
- Flujo de aprobación de cambios por parte del admin.  
- Certificados automáticos de asistencia.  
- API pública de calendario (Google Calendar / iCal).
