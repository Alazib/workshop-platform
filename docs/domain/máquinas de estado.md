# Máquinas de Estados — Session & Registration  
*Fase 1 — Workshop Platform*

Este documento describe las **máquinas de estado del dominio** para dos entidades claves:

- **Session** (unidad operativa del taller, incluye fechas, venue, aforo y visibilidad)  
- **Registration** (participación del usuario en una sesión concreta)

El objetivo es dejar completamente claras las reglas de transición, los estados permitidos,  
quién puede realizar cada cambio y bajo qué condiciones.

---

# 1. Máquina de estados de Session

## 1.1 ¿Qué representa cada estado de `Session`?

- **draft**  
  Sesión en borrador.  
  Puede no tener fechas, venue ni capacidad cerrada.  
  No es visible para el público y no permite inscripciones.

- **announced**  
  Sesión anunciada públicamente, pero aún no abierta a inscripciones.  
  Puede tener fechas provisionales o incompletas.  
  Sirve para mostrar que un evento “está en camino”.

- **published**  
  Sesión con todos los datos definitivos (fechas, venue, aforo)  
  y **abierta a inscripciones**.  
  Estado normal de operatividad.

- **full**  
  La sesión ha alcanzado su aforo máximo (`reserved + confirmed`).  
  No permite nuevas inscripciones salvo que se liberen plazas  
  y vuelva a `published`.

- **cancelled**  
  La sesión se cancela por decisión del organizador.  
  Afecta automáticamente a todas las inscripciones,  
  que pasan a `cancelled_by_organizer`.

- **postponed**  
  La sesión se pospone (cambio de fecha importante).  
  Indica que se realizará más adelante, pero la nueva fecha  
  aún no está fijada o la sesión no está lista para inscripciones.

- **completed**  
  La sesión ya ha tenido lugar.  
  Se procesan asistencias:  
  - `confirmed → attended` por defecto,  
  - y el organizador marca ausencias (`attended → no_show`).

- **archived**  
  Estado final para histórico.  
  La sesión ya no se modifica y solo existe para reportes o consulta.

---

## 1.2 Transiciones de estados — `Session`

| Desde      | Hacia        | Quién lo dispara             | Condición / Comentario |
|----------- |------------- |----------------------------- |------------------------|
| —          | draft        | Sistema / Admin              | Creación inicial |
| draft      | announced    | Admin / Organizer            | Se anuncia públicamente sin abrir inscripción |
| draft      | published    | Admin / Organizer            | Datos completos y se abre inscripción |
| announced  | draft        | Admin / Organizer            | Vuelve a edición oculta |
| announced  | published    | Admin / Organizer            | Se abre inscripción |
| published  | full         | Sistema                      | Aforo alcanzado (`reserved + confirmed == capacity_max`) |
| full       | published    | Admin / Organizer            | Se liberan plazas o se amplía aforo |
| published  | cancelled    | Admin / Organizer            | Cancelación antes de celebrarse |
| full       | cancelled    | Admin / Organizer            | Sesión llena que se cancela |
| published  | postponed    | Admin / Organizer            | Cambio de fecha relevante |
| full       | postponed    | Admin / Organizer            | Igual que arriba |
| postponed  | published    | Admin / Organizer            | Nueva fecha fijada y se reabre inscripción |
| published  | completed    | Sistema                      | La sesión finaliza |
| full       | completed    | Sistema                      | La sesión finaliza |
| completed  | archived     | Sistema / Admin              | Archivado tras completarse |
| cancelled  | archived     | Sistema / Admin              | Archivado tras cancelación |

> `archived` es un estado terminal: no se contemplan transiciones posteriores.

---

# 2. Máquina de estados de Registration

## 2.1 ¿Qué representa cada estado de `Registration`?

- **reserved**  
  Reserva manual creada por un organizador o admin.  
  No hay pago asociado.  
  Bloquea una plaza a nivel de aforo.  
  Uso excepcional (cupos, invitados, compromisos).

- **confirmed**  
  Inscripción confirmada mediante pago correcto  
  (`charge/paid` y `net_amount ≥ agreed_price`).  
  El usuario tiene derecho a asistir.

- **attended**  
  El usuario ha asistido a la sesión.  
  Se asigna automáticamente al finalizar la sesión,  
  excepto aquellos que el organizador marque como `no_show`.

- **no_show**  
  El usuario no asistió a la sesión.  
  Lo marca el organizador después de la revisión real de asistencia.  
  No da derecho a devolución.

- **cancelled_by_user**  
  Cancelación voluntaria del usuario, válida solo si se solicita  
  **con ≥ 7 días de antelación** al inicio de la sesión.  
  Genera un reembolso mediante `Payment(type='refund')`.

- **cancelled_by_organizer**  
  Cancelación provocada por decisiones del organizador  
  o porque la sesión pasa a `cancelled`.  
  Genera reembolso total automáticamente.

---

## 2.2 Transiciones de estados — `Registration`

| Desde                | Hacia                    | Quién lo dispara        | Condición / Comentario |
|----------------------|--------------------------|-------------------------|------------------------|
| —                    | reserved                 | Organizador/Admin       | Reserva manual sin pago |
| —                    | confirmed                | Sistema (tras pago)     | Solo si `Payment.type = charge` y `Payment.status = paid` y `net_amount ≥ agreed_price` |
| reserved             | confirmed                | Sistema (tras pago)     | Solo si `Payment.type = charge` y `Payment.status = paid` y `net_amount ≥ agreed_price` |
| reserved             | cancelled_by_organizer   | Organizador/Admin       | Se libera la plaza reservada |
| confirmed            | cancelled_by_user        | Usuario                 | Solicitud ≥ 7 días antes del inicio (con refund) |
| confirmed            | cancelled_by_organizer   | Sistema/Organizador     | Sesión cancelada o inscripción anulada por organización |
| confirmed            | attended                 | Sistema                 | La sesión finaliza |
| attended             | no_show                  | Organizador/Admin       | El organizador marca ausencia real |
| reserved/confirmed   | cancelled_by_organizer   | Sistema                 | La sesión pasa a `cancelled` |

> Estados terminales: `cancelled_by_user`, `cancelled_by_organizer`, `no_show`, `attended`.

---

# 3. Notas finales

## 3.1 Transiciones gobernadas por invariantes fuertes del dominio (solo sistema)

Son aquellas transiciones que **no debería forzar directamente un admin** cambiando el estado manualmente porque están ligadas a **invariantes del dominio** (aforo real, tiempo real, pagos reales).

En estos casos, el admin corrige **las causas** (datos) y es el sistema quien recalcula el estado.

### Session — transiciones con invariantes fuertes

- **`published → full` (Session)**  
  - **Quién:** Sistema.  
  - **Motivo (invariante):**  
    `full` significa “no hay plazas libres de verdad”, es decir:  
    ```text
    reserved + confirmed == capacity_max
    ```  
    Si un admin pudiera poner una sesión en `full` con 3 personas de 20,  
    los listados y métricas mentirían.
  - **Qué puede hacer el admin en su lugar:**  
    - Crear o cancelar inscripciones (`Registration`),  
    - cambiar `capacity_max`,  
    y dejar que el sistema decida si está `full` o no.
  - **Ejemplo:**  
    - La sesión tiene 10 plazas, 10 `confirmed`.  
    - Al entrar la última inscripción, el sistema pasa a `full`.  
    - Si un usuario cancela, el admin cancela la inscripción →  
      el conteo ya no llega a 10 → el sistema puede volver a `published`.

- **`published → completed` / `full → completed` (Session)**  
  - **Quién:** Sistema.  
  - **Motivo (invariante):**  
    `completed` significa “la sesión ya ha ocurrido en el tiempo real”.  
    Debería depender de `ends_at` y la fecha actual, no de una decisión manual arbitraria.  
  - **Qué puede hacer el admin en su lugar:**  
    - Corregir la fecha/hora de la sesión si estaba mal.  
    - Disponer de una acción tipo “forzar cierre” que internamente  
      vuelva a evaluar las reglas (no cambiar el estado directamente en la base).  
  - **Ejemplo:**  
    - La sesión terminó ayer pero por un fallo de un job sigue en `published`.  
    - El admin usa un botón de “reprocesar estado” →  
      el sistema comprueba fechas y la marca como `completed`.

### Registration — transiciones con invariantes fuertes

- **`— → confirmed` y `reserved → confirmed` (Registration)**  
  - **Quién:** Sistema (tras pago correcto).  
  - **Motivo (invariante):**  
    `confirmed` significa que el usuario ha pagado (o el pago está validado)  
    y que `net_amount ≥ agreed_price`.  
    Un admin no debería marcar “confirmado” si no hay un `Payment` coherente.
  - **Qué puede hacer el admin en su lugar:**  
    - Registrar un pago manual (`Payment` con `type='charge', status='paid'`),  
      por ejemplo si alguien pagó por transferencia.  
    - A partir de ahí, el sistema puede marcar `Registration` como `confirmed`.
  - **Ejemplo:**  
    - El usuario hace una transferencia bancaria;  
      la pasarela no interviene, pero el admin la ve en el extracto y crea un `Payment` manual.  
      El sistema detecta el cobro y pasa la inscripción a `confirmed`.

- **`confirmed → cancelled_by_user` (Registration)**  
  - **Quién:** Usuario (auto-servicio) + lógica de tiempo.  
  - **Motivo (invariante):**  
    Depende de la política de cancelación (≥ 7 días antes del inicio).  
    No debería depender del criterio puntual del admin.  
  - **Qué puede hacer el admin en su lugar:**  
    - Registrar que “el usuario ha solicitado la cancelación”,  
      y el sistema comprueba si cumple el plazo de los 7 días.  
    - Si se quiere hacer una excepción, se puede usar `cancelled_by_organizer`  
      (porque entonces ya no es la política estándar de usuario).
  - **Ejemplo:**  
    - El usuario llama 3 días antes protestando.  
      Legalmente no cumple el plazo. El admin puede:  
      - Mantener la inscripción (acabará como `no_show` si no va), o  
      - Cancelarla como `cancelled_by_organizer` si decide hacer una excepción con refund.

Resumen:  
- Estas transiciones se **calculan por reglas** (aforo, fechas, pagos).  
- El admin corrige los **datos de entrada**, no el estado directamente.

---

## 3.2 Transiciones administrables (el admin sí puede tocarlas directamente)

Aquí entran las transiciones que **son más operativas** y no rompen invariantes fuertes si el admin las usa con criterio.

### Ejemplos en Session

- `draft ↔ announced`  
  - El admin decide si enseñar o no la sesión en catálogo.  
  - Es puro control editorial; no afecta a pagos ni aforo.

- `announced ↔ published`  
  - Abrir o cerrar inscripciones cuando ya están los datos listos.

- `full → published`  
  - Mientras se respeten las reglas de aforo, el admin puede:  
    - ampliar `capacity_max`,  
    - o cancelar inscripciones,  
    y luego reabrir la sesión a inscripciones (estado `published`).

- `postponed ↔ published`  
  - Se pospone y luego se fija nueva fecha.  
  - El admin controla cuándo reabrir o volver a hacer visible para inscripción.

- `completed → archived` / `cancelled → archived`  
  - Transición de “limpieza”:  
    decidir cuándo se archivan del todo las sesiones.

**Ejemplo:**  
- Un taller se pospone porque el local está en obras (`published → postponed`).  
- Se acuerda nueva fecha con el espacio, el admin actualiza `starts_at` y `ends_at`  
  y vuelve a poner la sesión en `published`.

### Ejemplos en Registration

- `attended ↔ no_show` (o al menos `attended → no_show`)  
  - El organizador revisa la lista y arregla errores.  
  - Si en un futuro permites corregir, podrías aceptar también `no_show → attended`.

- `reserved → cancelled_by_organizer`  
  - El admin libera reservas no usadas.  
  - No afecta a pagos porque no había ninguno.

- `confirmed → cancelled_by_organizer` (caso individual)  
  - El admin puede anular una inscripción concreta (por ejemplo, problema de conducta, error, etc.)  
  - Genera el flujo de refund correspondiente.

**Ejemplo:**  
- El organizador pasa lista y pone `attended` a todos por defecto.  
  Luego ve que 2 personas ni aparecieron y los marca como `no_show`.  


