# Roles y Historias de Usuario — Versión 3 (modelo centralizado)

## Roles
| Rol | Descripción | Permisos clave |
|------|--------------|----------------|
| **admin** | Es la autoridad principal de la plataforma. Crea talleres, categorías, políticas y asigna organizadores a cada taller. Gestiona los pagos, las cancelaciones y los reportes financieros. | Crear/editar talleres, sesiones, categorías, usuarios y organizadores; configurar pasarelas de pago; validar transferencias; ver métricas globales y reportes financieros. |
| **organizer** | Persona que imparte uno o varios talleres. No puede crear ni modificar talleres, pero puede ver los talleres que se le asignan, sus sesiones, horarios, inscritos y estadísticas de asistencia. | Consultar los talleres que imparte; ver inscritos; descargar lista; ver estadísticas. |
| **attendee** | Usuario participante que se inscribe y paga. | Ver talleres, inscribirse, pagar, cancelar dentro de la política global de desistimiento. |
| **accountant (opcional)** | Perfil de solo lectura para informes económicos. | Ver reportes y exportes financieros. |

---

## Historias de usuario principales
1. Como **admin**, quiero **crear talleres** y asignar uno o varios organizadores a cada uno.  
2. Como **admin**, quiero **gestionar pagos** y confirmar manualmente los que sean por transferencia.  
3. Como **admin**, quiero **configurar categorías**, **políticas de cancelación** y **credenciales de pago** (Stripe, PayPal, Bizum).  
4. Como **organizer**, quiero **ver los talleres que imparto**, sus sesiones y los inscritos.  
5. Como **attendee**, quiero **inscribirme** y **pagar** mi plaza en un taller.  
6. Como **attendee**, quiero **recibir confirmación automática** de pago y recordatorio antes de cada sesión.  
7. Como **attendee**, quiero **cancelar mi inscripción** dentro de los plazos establecidos y recibir reembolso según la política global.  
8. Como **admin**, quiero **ver estadísticas generales** (ingresos, talleres, usuarios) y exportarlas a CSV.  
9. Como **organizer**, quiero **ver estadísticas de asistencia** de los talleres que imparto.  

---

## Reglas de negocio consolidadas

- Solo el **admin** puede crear o modificar talleres, categorías, políticas y usuarios.  
- El **organizer** no puede editar talleres; solo consultarlos.  
- Cada taller puede tener **uno o varios organizadores**.  
- Un taller pertenece a una **categoría** y puede tener **una o varias sesiones**.  
- Todos los cobros se realizan mediante las cuentas del **admin**.  
- Política de cancelación **global** conforme a la legislación española/europea (incluye derecho de desistimiento).  
- Tipos de pago:
  - **Automáticos:** Stripe, PayPal, Bizum → confirmación por webhook.
  - **Manual:** Transferencia → validación manual por el admin.
- Estados de inscripción:
  - `pending` → pago iniciado  
  - `paid` → pago recibido  
  - `confirmed` → plaza asegurada  
  - `cancelled` → cancelación o pago expirado

---

## Futuras ampliaciones previstas
- Sistema de lista de espera.  
- Flujo de aprobación de cambios (solicitud de modificación por organizer → validación del admin).  
- Certificados automáticos de asistencia.  
- API pública para sincronizar calendario (Google Calendar / iCal).
