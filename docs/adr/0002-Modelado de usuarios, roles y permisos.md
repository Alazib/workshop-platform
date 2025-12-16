# ADR 0002 — Modelado de usuarios, roles y permisos

*Status:* Accepted  
*Fecha:* YYYY-MM-DD

## Contexto
El sistema requiere distinguir tres tipos de usuario principales: Admin, Organizer y Attendee.  
Algunos usuarios (p. ej. administradores que también imparten talleres) deben poder asumir varios roles simultáneamente sin duplicar su cuenta.

## Decisión
- Implementar un modelo **User ↔ Role N:M** mediante una tabla puente `UserRole`.
- Mantener un catálogo `Role` con nombres normalizados (ADMIN, ORGANIZER, ATTENDEE).
- Añadir una entidad `OrganizerAssignment` que relacione organizadores con talleres específicos.
- Los permisos se derivarán de los roles asociados (RBAC).
- El frontend mostrará vistas diferentes según el rol activo, permitiendo cambiar de contexto en la UI.

## Alternativas consideradas
| Alternativa | Ventajas | Inconvenientes |
|--------------|-----------|----------------|
| **Relación N:1 User→Role** | Simplicidad inicial | No permite multirol, requeriría duplicar cuentas |
| **Herencia por tablas (Admin, Organizer, Attendee)** | Separación de datos | Mayor complejidad, JOINs costosos, difícil mantener |
| **N:M User↔Role** (→ Elegida) | Flexible, escalable, soporta multirol | Requiere gestión adicional de permisos y UI de cambio de rol |

## Consecuencias
- Los usuarios pueden combinar roles sin duplicar su identidad.
- La lógica de autorización será más rica y escalable.
- La UI incluirá un selector de “rol activo”.
- Añadiremos `OrganizerAssignment` para limitar el acceso a talleres concretos.

## Plan de implementación
1. Definir tablas `User`, `Role`, `UserRole`, `OrganizerAssignment`.
2. Incluir roles en el token JWT (campo `roles`).
3. Implementar control de vistas y rutas según rol activo.

## Referencias
- *NIST RBAC Model* (ISO/IEC 13250)
- *Django auth groups & permissions*
- *Spring Security RoleHierarchy documentation*
