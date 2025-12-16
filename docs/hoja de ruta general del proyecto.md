# 🗺️ Project Overview — Workshop Platform (Hoja de Ruta)

Esta hoja de ruta sustituye al documento anterior y refleja la estrategia actual del proyecto basada en:

- Arquitectura Hexagonal (Ports & Adapters)
- MVP rápido sobre Django
- Iteraciones mediante vertical slices
- Dominio estable y framework intercambiable
- Enfoque profesional apto para portfolio y entrevistas

---

# 🎯 Objetivo general

Construir una plataforma profesional para la gestión de talleres y eventos culturales, diseñada como proyecto de portfolio que demuestre:

- Modelado de dominio real
- Arquitectura hexagonal
- Documentación técnica (ADRs, diagramas)
- Capacidad de evolución y migración de frameworks
- Desarrollo por vertical slices (enfoque moderno en equipos senior)

---

# 🧭 Estructura de fases

Enfoque incremental basado en MVP + iteraciones.

---

# 🏗️ Fase 0 — Preparación y gobernanza
**Estado:** Completada parcialmente

**Objetivo:** Crear el esqueleto del proyecto y la documentación inicial.

**Tareas:**
- Crear repositorio y estructura básica.
- Añadir README inicial.
- Configurar `.gitignore`.
- Crear la carpeta `/docs/`.
- Abrir Issues y tablero Kanban.
- Definir formato de ADRs.
- Añadir `CURRENT_TASK.md`.

---

# 🧩 Fase 1 — Modelado del dominio
**Estado:** COMPLETADA

**Objetivo:** Cerrar las reglas de negocio y dejar el dominio “blindado”.

**Tareas completadas:**
- Historias de usuario.
- Roles y permisos.
- Entidades y relaciones.
- Máquinas de estado (Session, Registration).
- Política de cancelación y reembolsos.
- ADRs principales del dominio.

**Entregables:**
- `/docs/domain/roles e historias.md`
- `/docs/domain/entidades y relaciones.md`
- `/docs/domain/máquinas de estado.md`
- ADR 0004, 0005, 0007, 0008

---

# ⚙️ Fase 2 — Arquitectura + MVP Backend
**Estado:** EN PROGRESO

**Objetivos:**

1) Construir el backend mínimo funcional usando arquitectura hexagonal + Django.

2) Crear el "core workflow" del MVP: Inscripción → Pago simulado → Confirmación → Cancelación → Listado


Este MVP debe permitir:
- Ver sesiones publicadas
- Inscribirse
- Pagar (simulado)
- Confirmación
- Cancelación por usuario/organizador
- Listado de inscripciones

La arquitectura ya está definida en los ADR:

- **ADR 0009 — Arquitectura Hexagonal**
- **ADR 0010 — Django para el MVP + migración futura a Spring Boot**

**Resultados al finalizar esta fase:**
- Capa de dominio completa (Python puro)
- Casos de uso del MVP implementados
- Repositorios in-memory + adaptadores Django
- Endpoints REST funcionando
- Tests unitarios + de integración
- Documentación actualizada

**Importante:**
**Todo el desarrollo será por vertical slices**, no por capas completas.

---

# 🧗‍♂️ Fase 3 — Iteraciones del backend (vertical slices)

**Objetivo:** Añadir funcionalidades incrementales al backend *uno por uno*, cada una como un slice vertical. También "endurecer" el admin para que esté alineado con el dominio y no pueda saltarse las reglas de negocio.

Cada slice incluye:
- Dominio (si afecta)
- Caso de uso
- Endpoint(s)
- Repositorios
- Tests
- Documentación

## Slices backend propuestos (orden recomendado):
1. Autenticación básica (tokens simples o JWT)
2. CRUD de Workshops
3. CRUD de Sessions + asignación de venues
4. Gestión de descuentos
5. Gestión de organizers por sesión
6. Gestión de pagos reales (Stripe)
7. Reembolsos automáticos (Stripe)
8. Reporting básico para admin
9. Notificaciones (email)
10. Exportaciones CSV/Excel
11. Alinear admin con el domino (¿en última posición? Revisar el orden)

**Nota:**
Cada slice produce una funcionalidad lista para demostración.

---

# 🎨 Fase 4 — Frontend (React + TypeScript)
**Objetivo:** Crear la interfaz conectada al backend, también por slices.

## Slices frontend propuestos:
1. Login + persistencia de sesión
2. Listado de sesiones publicadas
3. Ficha de sesión
4. Flujo de inscripción + pago simulado
5. Panel del usuario
6. Panel admin (inscripciones, pagos)
7. Gestión de workshops y sesiones
8. Integración de pagos reales (Stripe JS)
9. Dashboard admin
10. Notificaciones y settings

---

# 💳 Fase 5 — Pagos reales y notificaciones
**Objetivo:** Llevar el proyecto a un nivel profesional incorporando pagos reales y comunicaciones.

**Tareas:**
- Integrar Stripe (primer objetivo)
- Posible integración con PayPal / Bizum
- Reembolsos automáticos vía webhook
- Notificaciones por email
- Recordatorios automáticos
- Selección de cola de mensajes (Celery o alternativas)

---

# 🔍 Fase 6 — Observabilidad
**Objetivo:** Mejorar calidad operacional.

**Tareas:**
- Logging estructurado
- Métricas
- Health checks
- Trazabilidad de flujos (OpenTelemetry opcional)
- Documentar SLOs y runbooks

---

# 🚀 Fase 7 — CI/CD y despliegue
**Objetivo:** Pipeline profesional y despliegue automatizado.

**Tareas:**
- Configurar CI (GitHub Actions / GitLab CI)
- Ejecutar tests + lint en cada PR
- Despliegue automático a Render / Railway / Vercel
- Tests E2E en pipeline

---

# 📚 Fase 8 — Documentación profesional + Portfolio final
**Objetivo:** Preparar la documentación para publicación profesional.

**Tareas:**
- Architecture Summary
- Diagramas actualizados
- ADRs finales
- Capturas de pantalla
- Screencast demo
- README final
- Preparar la presentación del portfolio

---

# 🧱 Entregables globales

- Backend con dominio claro y arquitectura hexagonal
- Frontend profesional y conectado
- Pagos y notificaciones
- Pipeline CI/CD funcionando
- Documentación completa del sistema
- Demostración pública
- Migración opcional demostrable de Django → Spring Boot

---

# 🔄 Flujo de trabajo general

- Cada fase = una Issue principal.
- Cada slice = subtareas/Issues asociadas.
- Cada PR = referencia a la Issue:

    feat: add registration payment slice [#14]
    fix: adjust cancellation rule [#23]

- La regla de oro:
  *"Siempre funcional, siempre demostrable, siempre incrementando valor."*

