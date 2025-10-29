# ADR 0006 — Modelado de la entidad Registration

*Status:* Accepted  
*Fecha:* YYYY-MM-DD  

---

## Contexto
La entidad `Registration` representa la inscripción de un usuario a una sesión (`Session`) concreta de un taller (`Workshop`).  
Debe gestionar estados de pago, asistencia y cancelación, reflejar condiciones legales (derecho de desistimiento)  
y mantener la trazabilidad de acciones tanto de usuarios como de organizadores.

---

## Decisión
- Se crea la entidad **`Registration`** con responsabilidad única: registrar la participación del usuario en una sesión.  
- Las relaciones y campos principales serán:
  - `user_id` → User (obligatorio)  
  - `session_id` → Session (obligatorio)  
  - `status` → enum  
  - `agreed_price` y `currency` (opcionales)  
  - `comments` (opcional) para observaciones, notas o motivos de cancelación.  

- Estados definidos:
  - Reserved, confirmed, attended, no_show, cancelled_by_user, cancelled_by_organizer


- **Flujo de estados:**

| Desde     | Hacia                    | Condición / Disparador                                                |
|------------|--------------------------|------------------------------------------------------------------------|
| —          | **reserved**             | Creación manual por organizador o administrador (sin pago).                           |
| — o reserved         | **confirmed**            | Pago completado.                                                      |
| reserved o confirmed  | **cancelled_by_organizer** | Anulación manual por organizador.                                    |
| reserved o confirmed  | **cancelled_by_organizer** | Cancelación de la sesión (reembolso total).                          |
| confirmed  | **cancelled_by_user**    | Solicitud ≥ 7 días antes del inicio (reembolso condicional).          |
| confirmed  | **attended**             | Asistencia automática al finalizar la sesión.                         |
| attended   | **no_show**              | Marcado manual por organizador si no asistió.                         |


- Reglas complementarias:
- `UNIQUE (user_id, session_id)` para evitar duplicados.  
- Las reservas (`reserved`) bloquean plaza hasta cancelación manual. La reserva tiene que bajo la identidad de una persona concreta.
- `Session.capacity_max` controla el aforo total; al alcanzarse, `Session.status → 'full'`.  
- Si `count(confirmed) < capacity_min` al llegar la fecha límite, la `Session` se cancela y todas las `Registration` pasan a `cancelled_by_organizer`.  
- La cancelación voluntaria (`cancelled_by_user`) solo es válida ≥ 7 días antes de `Session.starts_at`.  

---

## Consecuencias
- Lógica de pago desacoplada → módulo `Payment` gestionará `amount_paid`, `method`, `transaction_id`.  
- `Registration` mantiene `agreed_price` como “fotografía” del precio acordado, garantizando coherencia histórica.  
- Los estados de cancelación diferenciados simplifican reporting y gestión de reembolsos.  
- `comments` permite anotar motivos de cancelación, incidencias o comunicaciones internas.  

---

## Plan de implementación
1. Añadir la entidad y restricciones a `entities-and-relations.md`.  
2. Crear índice `UQ_registration_user_session`.  
3. Implementar job/evento post-sesión → `confirmed → attended`.  
4. Agregar lógica de cancelación con validación de plazo (7 días).  
5. Sincronizar cambios con la futura entidad `Payment`.

