# Entidades y Relaciones — borrador inicial

## Entidades
- User(id, first_name, last_name, country, city, email, phone, is_active, date_joined, date_left?, is_active)
- Role(id, name)
- UserRole(user_id, role_id, assigned_at)
- Workshop(id, title, description, category_id, capacity, base_price, status, is_active)
- OrganizerAssignment(user_id, workshop_id, assigned_at, is_active)
- Category(id, name)
- Session(id, workshop_id, starts_at, ends_at, venue_id?)
- Registration(id, user_id, workshop_id, session_scope?, status)
- Payment(id, registration_id, amount, method, status, paid_at)
- Discount(id, code, type, value, valid_from, valid_to, max_uses?, is_active)
- Policy(id, cancellation_window_hours, refund_rules_json)
- Notification(id, user_id, type, channel, status, sent_at, payload_json)
- Venue(id, name, address, city, is_active)
- City (id, name)
- Country (id, name)

## Relaciones
- User N:M Role (vía UserRole)
- User N:M Workshop (vía OrganizerAssignment para rol organizer)
- Workshop 1:N Session
- Workshop N:1 Category
- User N:M Workshop (vía Registration para rol attendee)
- Registration 1:1 Payment (o 1:N si permitimos reintentos)
- User N:1 City
- User N:1 Country
- City 1:N Venue
