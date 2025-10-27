# ADR 0004 — Modelado de la entidad Workshop

*Status:* Accepted  
*Fecha:* YYYY-MM-DD

## Contexto
El taller es la entidad central del sistema. Debe admitir múltiples modalidades (presencial, online o híbrida), estados de publicación y descuentos configurables.  
También debe permitir la creación por parte del administrador sin organizador asignado.

## Decisión
- Se crea una entidad `Workshop` con los campos definidos en `entities-and-relations.md`.
- El campo `format` refleja la intención general del curso (`physical`, `online`, `hybrid`).
- Las sedes y formatos específicos se manejarán a nivel de `Session`.
- El campo `status` gestionará el ciclo de vida completo del taller:
  - `draft`, `announced`, `published`, `full`, `cancelled`, `archived`.
- `Workshop` puede existir sin organizador (estado `draft`).
- Los descuentos se gestionan mediante una tabla `Discount` separada.
- El control de visibilidad se hará en base al `status`.

## Consecuencias
- Permite mostrar talleres en distintas fases (anunciados, llenos, históricos).
- Evita duplicación de entidades para modalidades.
- Separa intención (Workshop.format) de ejecución (Session.Venue).

## Plan de implementación
1. Añadir los campos descritos en `entities-and-relations.md`.
2. Crear validaciones:
   - `announced` no requiere fechas.
   - `published` requiere al menos una sesión.
   - `full` depende de la capacidad de las sesiones.
3. Añadir tests de visibilidad según rol y estado.
