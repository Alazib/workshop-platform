# ADR 0007 — Modelado de la entidad Payment (log de transacciones)

*Status:* Accepted  
*Fecha:* YYYY-MM-DD  

---

## Contexto

La plataforma necesita registrar los cobros y devoluciones asociados a las inscripciones (`Registration`)  
para poder gestionar pagos, reembolsos y auditoría financiera.

En la Fase 1 ya se ha decidido que:

- `Registration` representa la relación usuario–sesión (participación).
- `Payment` debe actuar como **log de transacciones**, no solo como un estado único.
- Se permite que una misma `Registration` tenga varios movimientos:
  - cobro inicial,
  - devoluciones,
  - reintentos de pago o fallos.

---

## Decisión

- La entidad **`Payment`** se modela como un **registro de operaciones económicas** ligadas a una inscripción:
  - Relación: `Registration 1 — N Payment`.
  - Cada fila de `Payment` representa **una transacción individual** (cobro o devolución).

### Campos principales

- `id` (UUID)
- `registration_id` (FK → Registration)
- `type` ∈ {`charge`, `refund`}
- `amount` (decimal, siempre positivo)
- `currency` (string(3))
- `status` ∈ {`pending`, `paid`, `refunded`, `failed`}
- `method` ∈ {`card`, `paypal`, `transfer`, `manual`}
- `transaction_ref` (nullable)
- `paid_at` (nullable)
- `notes` (nullable)
- `created_at`, `updated_at`

### Semántica de type + status

- `type = 'charge'`:
  - `status = 'pending'`: cobro iniciado pero no completado.
  - `status = 'paid'`: cobro realizado con éxito.
  - `status = 'failed'`: intento de cobro fallido.
  - `status = 'refunded'`: este cobro ha sido total o principalmente devuelto (ligado a uno o varios `refund`).

- `type = 'refund'`:
  - `status = 'pending'`: devolución solicitada/no completada.
  - `status = 'paid'`: devolución ejecutada (el dinero ha sido devuelto).
  - `status = 'failed'`: fallo en la devolución.
  - `status = 'refunded'` no aplica en la práctica a `refund`, pero se mantiene el mismo conjunto de estados por simplicidad de implementación.

### Relación con Registration

- `Registration` no almacena `payment_id`; se mantiene **independiente** del módulo de pagos.
- La relación se define como:
  ```text
  Payment.registration_id → Registration.id
  Registration 1 — N Payment

### Reglas de negocio clave

1. CONFIRMACIÓN DE INSCRIPCIÓN CUANDO:
   
   ````
   net_amount >= agreed_price y existe al menos un Payment(type='charge', status='paid')
   
   donde

   net_amount = SUM(amount WHERE type='charge' AND status='paid') - SUM(amount WHERE type='refund' AND status='paid')

3. DEVOLUCIONES Y CANCELACIONES:

Si una devolución está asociada a cancelled_by_user (con más de 7 días de antelación):
- Se crea un Payment con type='refund', status='paid' cuando la pasarela confirme la devolución.
- Se puede marcar el cobro original (charge) como status='refunded'.

Si la cancelación es por parte del organizador (cancelled_by_organizer):
- Mismo proceso, pero disparado por la lógica de cancelación de sesión.

3. PAGOS ACTIVOS:

Puede haber múltiples Payment por inscripción, pero se recomienda aplicar una validación de dominio:  
````
no más de un charge en pending o paid que supere el agreed_price sin estar equilibrado por refund


  
