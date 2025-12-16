# ADR 0003 — Estrategia de bajas lógicas (is_active)

*Status:* Accepted  
*Fecha:* YYYY-MM-DD

## Contexto
Algunas entidades del sistema requieren conservar su historial y permitir reactivación futura.  
Eliminar registros físicamente puede romper integridad referencial y dificultar auditorías o recuperación de datos.

## Decisión
Implementar un campo booleano `is_active` en las entidades con ciclo de vida gestionable:
- `User`
- `Workshop`
- `OrganizerAssignment`
- `Discount`
- `Venue` (opcional)
- `Category` (opcional)

Las entidades transaccionales (`Payment`, `Registration`, `Notification`, etc.) no usarán baja lógica: conservarán siempre sus registros históricos.

## Consecuencias
- Permite suspender o reactivar usuarios, talleres u organizadores sin pérdida de información.
- Simplifica el cumplimiento de normas de trazabilidad (RGPD, auditoría).
- Requiere incluir `WHERE is_active = true` en las consultas activas.
- Los borrados físicos se reservarán para datos temporales (tokens, logs, etc.).

## Plan de implementación
1. Añadir campo `is_active` a las entidades indicadas.
2. Incluir índice sobre `is_active` para optimizar consultas.
3. Crear servicio de administración para listar inactivos y reactivarlos.
