# Roles y Historias de Usuario — Versión 2 (decisiones revisadas)

## Roles
| Rol | Descripción | Permisos clave |
|------|--------------|----------------|
| **admin** | Responsable de toda la plataforma. Configura pasarelas de pago, gestiona usuarios y políticas. | Gestionar organizadores, aprobar pagos, crear categorías, modificar políticas, ver métricas. |
| **organizer** | Crea y gestiona sus propios talleres dentro de categorías definidas. | Crear/editar talleres y sesiones, gestionar inscritos de sus talleres, consultar estadísticas. |
| **attendee** | Usuario participante que se inscribe y paga. | Ver talleres, inscribirse, pagar, cancelar dentro de la política de desistimiento. |
| **accountant (opcional)** | Solo lectura de información financiera. | Ver reportes y exportes financieros. |

---

## Historias de usuario principales
1. Como **organizer**, quiero **crear un taller** (nombre, descripción, categoría, sesiones, fechas, precios, descuentos) para ofrecerlo al público.  
2. Como **attendee**, quiero **inscribirme** en un taller y **pagar** (Stripe / PayPal / Bizum / transferencia) para asegurar mi plaza.  
3. Como **admin**, quiero **gestionar pagos pendientes de transferencia** para confirmar manualmente las inscripciones.  
4. Como **attendee**, quiero **recibir confirmación automática** cuando se verifique mi pago.  
5. Como **attendee**, quiero **cancelar mi inscripción** y recibir reembolso según la política global de cancelación.  
6. Como **admin**, quiero **definir categorías** (literatura, música, cine, escritura...) para organizar los talleres.  
7. Como **organizer**, quiero **ver estadísticas de asistencia y ventas** de mis talleres.  
8. Como **admin**, quiero **ver métricas globales** de la plataforma y reportes financieros.  
9. Como **attendee**, quiero **recibir recordatorios automáticos** antes de cada sesión de un taller.  
10. Como **organizer**, quiero **ofrecer descuentos** o precios especiales para ciertos talleres o fechas.

---

## Reglas de negocio consolidadas
- Solo `admin` y `organizer` pueden crear talleres.  
  - `organizer` solo gestiona los suyos.  
- Un **taller** pertenece a una **categoría** y puede tener **múltiples sesiones/fechas**.  
- Todos los cobros se realizan a través de las cuentas del **admin**, quien luego gestiona las liquidaciones internas.  
- Política de cancelación **global**, conforme a la legislación española/europea (incluye derecho de desistimiento).  
- Tipos de pago:
  - **Automáticos:** Stripe, PayPal, Bizum → confirmación por webhook.
  - **Manual:** transferencia bancaria → confirmación por el admin.
- Estados de inscripción:
  - `pending` → pago iniciado.  
  - `paid` → pago recibido/verificado.  
  - `confirmed` → plaza asegurada.  
  - `cancelled` → cancelación o pago vencido.  

---

## Futuras ampliaciones previstas
- Sistema de lista de espera (si el taller está completo).  
- Certificados automáticos de asistencia.  
- API pública para sincronizar calendario (Google Calendar / iCal).  
