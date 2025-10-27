# Entidades y Relaciones — Fase 1.2

Este documento define las entidades principales del dominio y sus relaciones iniciales.  
El objetivo es capturar el modelo conceptual del sistema de gestión de talleres y eventos culturales,  
manteniendo la trazabilidad de las decisiones arquitectónicas mediante ADRs.

---

## User

Representa a cualquier persona que interactúa con el sistema: administradores, organizadores y asistentes.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único del usuario |
| **first_name** | string | Nombre |
| **last_name** | string | Apellidos |
| **email** | string | Correo electrónico (único) |
| **phone** | string | Teléfono de contacto |
| **is_active** | boolean | Baja lógica del usuario (suspender/reactivar) |
| **date_joined** | datetime | Fecha de alta |
| **date_left** | datetime (nullable) | Fecha de baja definitiva |
| **created_at** | datetime | Creación de registro |
| **updated_at** | datetime | Última modificación |

Relaciones:

User

├─ N:M → Role (vía UserRole)

├─ N:M → Workshop (vía Registration solo para rol attendee)

└─ N:M → Workshop (vía OrganizerAssignment rolo para rol organizer)



---

## Role

Catálogo de roles posibles dentro del sistema.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **name** | string | Nombre del rol (`ADMIN`, `ORGANIZER`, `ATTENDEE`) |
| **description** | string | Descripción funcional del rol |
| **created_at** | datetime | Fecha de creación |
| **updated_at** | datetime | Última modificación |

> Nota: No tiene `is_active` (gestión simple de catálogo).  
> Cambios de roles se manejan vía `UserRole`.

---

## UserRole

Tabla intermedia para relación N:M entre `User` y `Role`.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **user_id** | FK(User) | Usuario |
| **role_id** | FK(Role) | Rol |
| **assigned_at** | datetime | Fecha de asignación |

---

## OrganizerAssignment

Relaciona organizadores con talleres específicos.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **user_id** | FK(User) | Organizador asignado |
| **workshop_id** | FK(Workshop) | Taller asociado |
| **assigned_at** | datetime | Fecha de asignación |
| **is_active** | boolean | Baja lógica del vínculo (pausar/rehabilitar) |

---

## Category

Catálogo de categorías (ej. “Espacio para Cine”, “Espacio para Literatura”, etc.).

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **name** | string | Nombre |
| **description** | string | Descripción |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

> Nota: Sin `is_active` (catálogo estable).  
> Si se elimina, se migra/rehace la relación en `Workshop`.

---

## Discount

Define descuentos o promociones aplicables a talleres específicos.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **workshop_id** | FK(Workshop) | Taller al que aplica |
| **code** | string | Código promocional (opcional) |
| **type** | enum(`'percentage'`, `'fixed'`) | Tipo de descuento |
| **value** | decimal | Valor o porcentaje |
| **valid_from** | datetime | Inicio de validez |
| **valid_to** | datetime | Fin de validez |
| **max_uses** | int | Límite de usos (opcional) |
| **is_active** | boolean | Activar/desactivar sin borrar |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

---

## Venue

Lugar (físico o virtual) donde se imparte un taller o una sesión.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **name** | string | Nombre o etiqueta |
| **type** | enum(`'physical'`, `'online'`, `'hybrid'`) | Tipo de sede |
| **address** | string (nullable) | Dirección si es presencial |
| **city** | string (nullable) | Ciudad/localidad |
| **online_url** | string (nullable) | Enlace al aula virtual |
| **is_active** | boolean | Activar/desactivar sede |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

---

## Workshop

Representa un curso, taller o actividad cultural.

### Descripción
Unidad principal de oferta: puede ser presencial, online o híbrida; pasa por estados de ciclo de vida; puede tener múltiples sesiones y varios organizadores; se puede crear en borrador.

### Campos

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador |
| **title** | string | Título |
| **description** | text | Descripción detallada |
| **category_id** | FK(Category) | Categoría principal |
| **format** | enum(`'physical'`, `'online'`, `'hybrid'`) | Modalidad general |
| **status** | enum(`'draft'`, `'announced'`, `'published'`, `'full'`, `'cancelled'`, `'archived'`) | Estado/visibilidad |
| **base_price** | decimal | Precio base |
| **image_url** | string | Portada/cartel |
| **language** | string(2) | Idioma (`es`, `en`, …) |
| **difficulty_level** | enum(`'beginner'`, `'intermediate'`, `'advanced'`) | Nivel |
| **venue_id** | FK(Venue, nullable) | Sede principal opcional (las sesiones pueden tener su propio venue) |
| **is_active** | boolean | Baja lógica del taller |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

### Estados (`status`)

| Estado | Visible por | Descripción |
|---------|-------------|-------------|
| `draft` | Admin y organizers asignados | Borrador |
| `announced` | Público | Anunciado, sin fechas |
| `published` | Público | Activo con sesiones |
| `full` | Público | Lleno (inscripción cerrada) |
| `cancelled` | Público | Cancelado/pospuesto |
| `archived` | Público | Histórico, solo lectura |


### Relaciones

Workshop

├─ belongs_to → Category

├─ has_many → Sessions

├─ has_many → OrganizerAssignments

├─ has_many → Registrations

└─ belongs_to → Venue (opcional)



### Notas
- Descuentos en entidad `Discount` (relación N:1).
- Aforo por `Session` (no en `Workshop`).
- Visibilidad controla `status` + rol del usuario.
- Puede existir sin organizer (borrador).

---

## Resumen global de relaciones

User N:M Role (UserRole)

User N:M Workshop (OrganizerAssignment solo para rol organizer)

User N:M Workshop (Registration solo para rol attendee)

Workshop 1:N Session

Workshop N:1 Category
Workshop N:1 Venue
Workshop 1:N Discount
Category 1:N Workshop


