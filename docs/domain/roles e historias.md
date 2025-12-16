# Roles y Historias de Usuario — Versión Definitiva (Fase 1 Completada)

Este documento define los **roles del sistema**, sus responsabilidades y el conjunto completo de **historias de usuario** necesarias para cubrir la operativa descrita en la Fase 1 del dominio.

Su propósito es servir como base funcional para:
- Diseño de casos de uso (Fase 2)
- Arquitectura backend
- Priorización de funcionalidades
- QA y criterios de aceptación

---

# 1. Roles del Sistema

| Rol | Descripción | Capacidades clave |
|------|-------------|-------------------|
| **admin** | Administrador global del sistema. Control total sobre catálogo, sesiones, inscripciones, pagos, usuarios y reportes. Puede haber varios. | Crear/editar talleres, sesiones, categorías y venues. Gestionar organizadores. Validar pagos manuales. Gestionar cancelaciones. Acceder a métricas y reportes financieros. |
| **organizer** | Persona responsable de impartir sesiones de uno o varios workshops. No crea talleres, pero gestiona su ejecución. | Ver sesiones asignadas, ver inscritos, marcar asistencias/no-shows, descargar listas, consultar estadísticas de asistencia. |
| **attendee** | Usuario participante que se inscribe en sesiones y realiza el pago. | Ver catálogo, inscribirse, pagar, cancelar dentro del plazo formal, recibir notificaciones y recordatorios. |
| **accountant (opcional)** | Perfil de solo lectura enfocado en la parte financiera. | Ver reportes económicos, exportar listados de transacciones. |

---

# 2. Historias de Usuario por Rol

Las historias están redactadas siguiendo la estructura:  
**Como [rol], quiero [acción], para [objetivo o beneficio].**

---

## 2.1 Historias de usuario — Rol: *admin*

### Gestión de talleres y catálogo
1. Como **admin**, quiero **crear un workshop** para poder publicarlo más adelante.
2. Como **admin**, quiero **crear sesiones** dentro de un workshop para definir fechas, modalidad, venue y aforo.
3. Como **admin**, quiero **editar o archivar un workshop** para mantener actualizado el catálogo.
4. Como **admin**, quiero **gestionar categorías** para clasificar los workshops.

### Gestión de usuarios y organizadores
5. Como **admin**, quiero **crear y gestionar cuentas de organizadores**, para asignarlos a sesiones.
6. Como **admin**, quiero **gestionar otros administradores** (crear, desactivar), para repartir responsabilidades.
7. Como **admin**, quiero **consultar los datos de attendees** para auditorías y comunicación legítima.

### Inscripciones y pagos
8. Como **admin**, quiero **ver todas las inscripciones de una sesión**, para revisar el aforo y resolver incidencias.
9. Como **admin**, quiero **registrar pagos manuales** (transferencias), para completar inscripciones sin pasarela.
10. Como **admin**, quiero **emitir devoluciones** cuando corresponda por normativa.
11. Como **admin**, quiero **cancelar inscripciones manualmente**, por incidencias reales.

### Lógica operativa de sesiones
12. Como **admin**, quiero **cancelar una sesión**, para que el sistema anule todas las inscripciones y haga los reembolsos.
13. Como **admin**, quiero **posponer una sesión**, para gestionar cambios de fecha sin perder información.

### Reportes y auditoría
14. Como **admin**, quiero **ver estadísticas globales**: ingresos, asistentes, no-shows, aforos, pagos.
15. Como **admin**, quiero **exportar reportes financieros** para contabilidad externa.

---

## 2.2 Historias de usuario — Rol: *organizer*

### Gestión del día a día
1. Como **organizer**, quiero **ver mis workshops y sesiones asignadas**, para preparar la actividad.
2. Como **organizer**, quiero **consultar la lista de inscritos**, para organizar la clase.
3. Como **organizer**, quiero **descargar un listado en PDF o Excel**, para control presencial.

### Asistencia y control
4. Como **organizer**, quiero **marcar asistencias y no-shows**, para completar la información después de la sesión.
5. Como **organizer**, quiero **ver estadísticas de asistencia** históricas.

### Comunicación
6. Como **organizer**, quiero **enviar mensajes operativos** a los inscritos (cambios menores, material necesario), sin acceder a datos fuera de su ámbito.

---

## 2.3 Historias de usuario — Rol: *attendee*

### Descubrimiento y registro
1. Como **attendee**, quiero **ver el catálogo de workshops** disponibles.
2. Como **attendee**, quiero **ver sesiones concretas**, con fechas, modalidad, lugar y precio.
3. Como **attendee**, quiero **inscribirme en una sesión**, para reservar una plaza.

### Pagos
4. Como **attendee**, quiero **pagar mi inscripción** mediante Stripe/PayPal/Bizum/transferencia, para confirmar mi plaza.
5. Como **attendee**, quiero **recibir confirmación automática**, para asegurarme de que el pago se ha procesado.

### Cancelaciones y reglas legales
6. Como **attendee**, quiero **cancelar la inscripción** si faltan ≥ 7 días, para recibir reembolso.
7. Como **attendee**, quiero **ver claramente la política de cancelación**, para saber si tengo derecho a devolución.

### Comunicaciones
8. Como **attendee**, quiero **recibir recordatorios automáticos**, para no olvidar la fecha.
9. Como **attendee**, quiero **dar o revocar mi consentimiento** para recibir información de futuros eventos.

---

## 2.4 Historias de usuario — Rol: *accountant* (opcional)

1. Como **accountant**, quiero **ver todas las transacciones financieras**, para validar ingresos y devoluciones.
2. Como **accountant**, quiero **exportar un libro mayor** de pagos y reembolsos.
3. Como **accountant**, quiero **filtrar por método de pago**, para conciliaciones bancarias.

---

# 3. Reglas de Negocio Asociadas (Resumen Fase 1)

### 3.1 Permisos y responsabilidades
- Solo **admins** crean/gestionan workshops, sesiones, categorías y organizadores.
- **Organizers** gestionan asistencia, no pagos.
- **Attendees** solo gestionan su propia inscripción.

### 3.2 Pagos
- Todos los pagos van a cuentas controladas por admin.
- Transferencias requieren validación manual.
- `Payment` funciona como log de transacciones, no como estado único.

### 3.3 Política de cancelación
- Cancelación voluntaria del usuario permitida **solo ≥ 7 días** antes del inicio.
- Cancelación por organizador → siempre con reembolso.
- No-show → sin devolución.

### 3.4 Aforo
- Los estados dependientes de aforo (`full`) son gestionados solo por el sistema.
- `reserved` y `confirmed` impactan en el cálculo del aforo.

---

# 4. Futuras Ampliaciones (Backlog)

- Lista de espera.
- Certificados automáticos de asistencia.
- API externa para exportar calendario.
- Envíos masivos segmentados (newsletter RGPD).
- Login social (Google/Apple).
- Panel avanzado de métricas (cohortes, retención).

---

# 5. Documentos Relacionados
- `/docs/domain/entities-and-relations.md`
- `/docs/domain/state-machines.md`
- `/docs/adr/0007-payment-model.md`
- `/docs/adr/0008-cancellation-and-refund-policy.md`
- `/docs/domain/roles-and-stories.md` (este documento)

---
