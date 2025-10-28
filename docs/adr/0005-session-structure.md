# ADR 0005 — Modelado de la entidad Session

*Status:* Accepted  
*Fecha:* YYYY-MM-DD

## Contexto
El taller (`Workshop`) es un concepto de catálogo/marketing. La ejecución real sucede en **sesiones** con fecha/hora, modalidad y aforo.  
Necesitamos que un workshop pueda ofrecer sesiones **físicas y online**, incluso en la misma franja horaria, pero cada sesión individual debe ser de **un único tipo**.

## Decisión
- Crear la entidad **`Session`** como unidad operativa con los campos:
  - `workshop_id` (obligatorio), `type` (`physical|online`), `status` (`draft|announced|published|full|cancelled|postponed|completed|archived`),
  - `starts_at`/`ends_at` (opcionales en `draft/announced`), `timezone` = `Europe/Madrid`,
  - `venue_id` (opcional en `draft/announced`), `capacity_min`, `capacity_max`,
  - `price_override` (opcional), `is_active`.
- **Workshop no tendrá `status` ni `venue_id`**: esos atributos viven en las sesiones.
- **Una sesión nunca es híbrida**: si se ofrece a la misma hora en físico y online, se crean **dos sesiones**.
- Las plazas libres se calculan a partir de `capacity_max` menos inscripciones activas (no se almacenan).
- **Inscripciones** (`Registration`) siempre referencian a **Session** (no a Workshop).

## Alternativas consideradas
- **Estado en Workshop**: confunde la operativa real (las sesiones tienen vida propia).  
- **Session híbrida** (`type = hybrid`): complejiza aforo, venue y entradas; preferimos dos sesiones separadas.

## Consecuencias
- Separación clara entre marketing (Workshop) y ejecución (Session).
- Validaciones condicionales por estado (en `draft/announced` se permite fecha/venue nulos).
- El filtrado por modalidad se realiza a nivel de Workshop (intención) y Session (ejecución real).
- Simplifica reglas de aforo y notificaciones.

## Plan de implementación
1. Añadir entidad `Session` con los campos decididos.
2. Migrar relaciones: `Registration` ahora apunta a `Session`.
3. Actualizar documentación y diagramas de relaciones.
4. Añadir tests de dominio (validaciones de estado/fechas/aforos).
