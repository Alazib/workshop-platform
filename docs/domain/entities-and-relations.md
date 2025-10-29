# Entidades y Relaciones — Fase 1.3

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
├─ N:M → Session (vía OrganizerAssignment, como organizer)  
└─ N:M → Session (vía Registration, como attendee)

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

Relaciona organizadores con sesiones específicas.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **user_id** | FK(User) | Organizador asignado |
| **session_id** | FK(Session) | Sesión asociada |
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

Lugar (físico o virtual) donde se imparte una **Session**.  
> Un Workshop es conceptual; el lugar solo aplica a la sesión concreta.

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

Representa un curso, taller o actividad cultural **conceptual** (qué es el curso).

### Descripción
Unidad principal de oferta: puede declararse como presencial, online o híbrida (intención general).  
No tiene estado operativo ni lugar físico; esas características se definen a nivel de **Session**.  
Puede tener múltiples sesiones y varios organizadores; se puede crear en borrador (sin organizers).

### Campos

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador |
| **title** | string | Título |
| **description** | text | Descripción detallada |
| **category_id** | FK(Category) | Categoría principal |
| **format** | enum(`'physical'`, `'online'`, `'hybrid'`) | Modalidad general (intención) |
| **base_price** | decimal | Precio base sugerido (puede sobreescribirse por sesión) |
| **image_url** | string | Portada/cartel |
| **language** | string(2) | Idioma (`es`, `en`, …) |
| **difficulty_level** | enum(`'beginner'`, `'intermediate'`, `'advanced'`) | Nivel |
| **is_active** | boolean | Baja lógica del taller |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

Relaciones:  
Workshop  
├─ has_many → Sessions  
├─ has_many → OrganizerAssignments  
└─ has_many → Discounts

> Notas:
> - La visibilidad operativa (borrador, publicado, lleno, etc.) vive en **Session**.  
> - Aforo por `Session` (no en `Workshop`).

---

## Session

Instancia **operativa** de un taller: cuándo y dónde sucede realmente.

### Reglas clave del dominio
- Una **Session** es **o física o online** (`type`), **nunca híbrida**.  
- En estados `draft` y `announced`, la fecha/hora y el `venue_id` **pueden ser nulos**.  
- Zona horaria del proyecto: **Europe/Madrid**.  
- Controla **aforo mínimo y máximo**. Las plazas libres se **calculan** (no se almacenan).

### Campos

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador |
| **workshop_id** | FK(Workshop) | Taller al que pertenece (obligatorio) |
| **type** | enum(`'physical'`, `'online'`) | Modalidad concreta de la sesión |
| **status** | enum(`'draft'`, `'announced'`, `'published'`, `'full'`, `'cancelled'`, `'postponed'`, `'completed'`, `'archived'`) | Estado operativo y visibilidad |
| **starts_at** | datetime (nullable en `draft/announced`) | Inicio |
| **ends_at** | datetime (nullable en `draft/announced`) | Fin |
| **timezone** | string | Siempre `Europe/Madrid` (documentado) |
| **venue_id** | FK(Venue, nullable en `draft/announced`) | Sede física/virtual concreta |
| **capacity_min** | int | Plazas mínimas (apertura/viabilidad) |
| **capacity_max** | int | Plazas máximas (aforo) |
| **price_override** | decimal (nullable) | Precio específico de la sesión (si distinto de `Workshop.base_price`) |
| **is_active** | boolean | Baja lógica de la sesión |
| **created_at** | datetime | Creación |
| **updated_at** | datetime | Última modificación |

> Plazas libres = `capacity_max` − `count(Registration where status in ['reserved','confirmed'])`  
> (Campo **derivado**, no se almacena.)

---

## Registration

Representa la inscripción de un usuario a una **Session** concreta de un taller.  
Gestiona los distintos estados del ciclo de vida de la participación y mantiene trazabilidad de precios, asistencias y cancelaciones.

| Campo | Tipo | Descripción |
|--------|------|-------------|
| **id** | UUID | Identificador único |
| **user_id** | FK(User) | Usuario inscrito |
| **session_id** | FK(Session) | Sesión específica (obligatoria) |
| **status** | enum(`reserved`, `confirmed`, `attended`, `no_show`, `cancelled_by_user`, `cancelled_by_organizer`) | Estado de la inscripción |
| **registration_date** | datetime | Fecha de creación |
| **confirmation_date** | datetime (nullable) | Fecha de confirmación del pago |
| **cancelled_date** | datetime (nullable) | Fecha de cancelación |
| **agreed_price** | decimal (nullable) | Precio acordado al momento de la inscripción |
| **currency** | string(3) (nullable) | Moneda correspondiente |
| **comments** | text (nullable) | Campo libre para observaciones, incidencias o motivos de cancelación |
| **created_by** | FK(OrganizerAssignment, nullable) | Organizador que creó o gestionó la inscripción |
| **source** | enum(`self`, `organizer`, `imported`) | Origen de la inscripción |
| **created_at** | datetime | Creación del registro |
| **updated_at** | datetime | Última modificación |

### Notas
- `agreed_price` refleja el **precio pactado** en el momento de la inscripción (incluyendo descuentos aplicados).  
  Su función es mantener trazabilidad comercial aunque el precio del Workshop cambie.  
- `amount_paid` no se guarda aquí, sino en la entidad `Payment`, que registra la transacción económica.  
- El campo `comments` sirve para cualquier observación: motivo de cancelación, incidencias, notas internas o feedback del participante.  
- `reserved` se usa únicamente para reservas manuales realizadas por un organizador.  
- Cancelaciones automáticas y voluntarias están diferenciadas en `cancelled_by_user` y `cancelled_by_organizer`.

Relaciones:

User 1 — N Registration N — 1 Session N — 1 Workshop
Registration 0..1 — 1 OrganizerAssignment (created_by)


Restricciones:
- UNIQUE (user_id, session_id)  
- Las reservas y confirmaciones cuentan para el aforo de Session.  
- Las cancelaciones del organizador actualizan automáticamente las inscripciones asociadas.

---

## (Avance) Payment — referencia mínima para relaciones

> **Pendiente**

### Payment (mínimo conceptual)
- `id`, `registration_id` (FK Registration), `amount`, `method`, `status`, `paid_at`.

---

## Resumen global de relaciones

User N:M Role (UserRole)  
User N:M Session (OrganizerAssignment, solo para users organizer)  
User N:M Session (Registration, solo para users attendee)  

Workshop 1:N Session  
Workshop 1:N Discount  
Workshop N:1 Category  

Session N:1 Workshop  
Session N:1 Venue  
Session 1:N Registration  

Payment N:1 Registration

