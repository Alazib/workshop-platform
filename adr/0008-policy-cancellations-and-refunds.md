# ADR 0008 — Política de Cancelación y Reembolso  
*Status:* Accepted  
*Fecha:* YYYY-MM-DD  

## Contexto

El sistema de inscripción y pagos de Workshop Platform necesita una **política clara, consistente y auditable** para manejar:

- cancelaciones voluntarias del usuario,  
- cancelaciones por parte del organizador,  
- reembolsos totales o parciales,  
- reservas sin pago,  
- cambios de asistencia,  
- relación entre `Registration` y `Payment`.

La plataforma usa:

- **Registration** → estado operativo del vínculo usuario–sesión.  
- **Payment** → log financiero con transacciones independientes (múltiples pagos, múltiples devoluciones).  

Este ADR define la política oficial de cancelación y reembolso según los requisitos de Fase 1.

---

## Decisión

### 1. Modelo financiero basado en transacciones (`Payment`)

- La entidad `Payment` registra **transacciones individuales**:
  - `charge` (pago)
  - `refund` (devolución)
  - intentos fallidos (`failed`)
- No se actualizan pagos pasados:  
  **todo es historizado** para auditoría.
- Una `Registration` puede tener **múltiples** transacciones.

---

### 2. Estados de Registration y su efecto financiero

| Estado de Registration | ¿Reembolso? | Quién lo puede poner | Condición |
|------------------------|-------------|----------------------|-----------|
| `reserved`             | No aplica   | Organizador/Admin    | No hay pago |
| `confirmed`            | No          | Sistema              | Pago válido |
| `cancelled_by_user`    | Sí          | Usuario (validado por sistema) | Solicitud ≥ 7 días |
| `cancelled_by_organizer` | Sí (total) | Organizador/Admin o sistema | Siempre |
| `attended`             | No          | Sistema              | Sesión finalizada |
| `no_show`              | No          | Organizador/Admin    | Ausencia real |

---

### 3. Regla principal: cancelación por usuario solo válida ≥ 7 días

Un usuario puede cancelar con derecho a reembolso **solo si**:
> fecha_solicitud_cancelación ≤ starts_at - 7 días


Si no cumple:

- la interfaz no permite `cancelled_by_user`,
- si el admin quiere hacer una excepción, debe usar `cancelled_by_organizer`.

---

### 4. Reglas de negocio clave

#### 4.1 Confirmación depende de un pago válido
Una inscripción pasa a `confirmed` solo cuando existe:

> Payment(type='charge', status='paid') Y net_amount_acumulado >= agreed_price


El admin **NO** confirma inscripciones manualmente;  
solo puede registrar pagos manuales (transferencias, caja, Bizum fuera de plataforma)  
y el sistema valida la transición.

---

#### 4.2 Cancelación del usuario exige cumplir la regla de 7 días
Si:

> hoy <= starts_at - 7 días


→ el usuario puede cancelar  
→ se genera `cancelled_by_user`  
→ se crea `Payment(type='refund')`.

Si no:

- el usuario no puede cancelar por sí mismo;
- el admin podrá usar `cancelled_by_organizer` en caso excepcional.

---

#### 4.3 Cancelación del organizador siempre reembolsa
Si la sesión pasa a `cancelled`, entonces:

> TODAS las Registration en estado reserved/confirmed → cancelled_by_organizer


y se generan los correspondientes `refund`.

---

### 5. Flujo de estados y pagos

#### 5.1 Flujo de estados relevante

| Desde | Hacia | Disparador |
|-------|-------|-----------|
| — | confirmed | Pago completado |
| reserved | confirmed | Pago completado |
| confirmed | cancelled_by_user | Solicitud válida ≥ 7 días |
| confirmed | cancelled_by_organizer | Sesión cancelada o decisión operativa |
| confirmed | attended | Finalización de la sesión |
| attended | no_show | Ajuste manual del organizador |

#### 5.2 Flujo financiero relevante

| Evento | Movimiento en Payment |
|--------|------------------------|
| Pago exitoso | `charge / paid` |
| Cancelación usuario válida | `refund / paid` |
| Cancelación organizador | `refund / paid` (100%) |
| No-show | No hay devolución |
| Cancelación usuario < 7 días | No permitido |

---

## Consecuencias

1. **Coherencia del dominio**  
   - No existe inscripción confirmada sin pago válido.
   - No existe devolución fuera de plazo salvo intervención explícita del organizador.

2. **Auditoría financiera robusta**  
   - Ningún pago se borra ni se modifica.  
   - Todas las transacciones quedan registradas.

3. **Separación limpia entre operativa y finanzas**  
   - `Registration` refleja la situación del usuario respecto a la sesión.  
   - `Payment` refleja el historial económico.

4. **Automatización segura y predecible**  
   - Cancelación de sesión → cascada automática de reembolsos.  
   - Fin de sesión → asistencias marcadas automáticamente.

5. **Base sólida para Fase 2**  
   - Lógica de backend clara (validaciones, hooks, jobs, límites temporales).

---

## Plan de Implementación

1. Validar transición a `confirmed` mediante pagos.  
2. Implementar comprobación temporal para `cancelled_by_user`.  
3. Implementar reembolsos automáticos para cancelaciones válidas y cancelaciones de sesión.  
4. Añadir eventos internos:
   - `onSessionCancelled`
   - `onSessionCompleted`
5. Añadir auditoría:
   - registro de actor,
   - timestamp,
   - notas de operación.




