# 🗺️ Project Overview — Workshop Platform

## 🎯 Objetivo general
Desarrollar una plataforma completa para la gestión de talleres y eventos culturales, con un enfoque profesional en **arquitectura de software**, **documentación**, **patrones de diseño** y **buenas prácticas**.

El proyecto se estructura en **fases secuenciales** que reflejan el ciclo de vida de un sistema profesional, desde el análisis del dominio hasta el despliegue y documentación final.

---

## 🧭 Fases y tareas principales

### 🏗️ Fase 0 — Preparación y gobernanza
**Objetivo:** Establecer la base del proyecto y los estándares iniciales.  
**Tareas:**
- Crear repositorio, estructura de carpetas y documentación base.
- Incluir README, .gitignore y ADR inicial.
- Configurar Issues y tableros de seguimiento.
- Crear documento `CURRENT_TASK.md`.

---

### 🧩 Fase 1 — Modelado del negocio
**Objetivo:** Comprender el dominio funcional antes de desarrollar código.  
**Tareas:**
1.1 Definir roles y escribir historias de usuario.  
1.2 Identificar entidades y relaciones.  
1.3 Crear el diagrama de dominio (ERD).  
1.4 Redactar los casos de uso principales.

**Entregables:**  
`/docs/domain/roles-and-stories.md`  
`/docs/domain/entities-and-relations.md`  
`/docs/domain/usecases.md`  

---

### ⚙️ Fase 2 — Diseño arquitectónico y setup técnico
**Objetivo:** Definir la arquitectura del sistema y preparar el entorno de desarrollo.  
**Tareas:**
2.1 Elegir el stack final (Django o Spring Boot).  
2.2 Definir la arquitectura (por capas / hexagonal).  
2.3 Diseñar la estructura de módulos y carpetas.  
2.4 Configurar entorno local con Docker y base de datos.

**Entregables:**  
`/docs/adr/0002-architecture-choice.md`  
`/docker-compose.yml`  
Primer endpoint `/health`.

---

### 💻 Fase 3 — Backend (API y dominio)
**Objetivo:** Implementar la lógica de negocio y los endpoints principales.  
**Tareas:**
3.1 Crear el esqueleto del backend.  
3.2 Implementar entidades principales (User, Workshop, Session, Payment, etc.).  
3.3 Añadir autenticación y roles (JWT o Auth estándar).  
3.4 Implementar CRUDs básicos.  
3.5 Añadir tests unitarios e integración.

---

### 🎨 Fase 4 — Frontend (React + TypeScript)
**Objetivo:** Desarrollar la interfaz de usuario y conectar con el backend.  
**Tareas:**
4.1 Configurar React + TypeScript.  
4.2 Crear componentes principales (Login, Dashboard, Talleres).  
4.3 Conectar con API (React Query / Axios).  
4.4 Añadir autenticación y rutas protegidas.  
4.5 Testing de componentes.

---

### 💳 Fase 5 — Pagos y notificaciones
**Objetivo:** Integrar pasarelas de pago y recordatorios automáticos.  
**Tareas:**
5.1 Integrar Stripe, PayPal y Bizum (pagos automáticos).  
5.2 Añadir validación manual para transferencias.  
5.3 Implementar notificaciones y recordatorios.  
5.4 Configurar colas de mensajes (Celery / RabbitMQ).

---

### 🔍 Fase 6 — Observabilidad y mantenimiento
**Objetivo:** Asegurar la operatividad y trazabilidad del sistema.  
**Tareas:**
6.1 Añadir logging estructurado y métricas.  
6.2 Configurar health-checks y tracing.  
6.3 Documentar SLOs y runbooks.

---

### 🚀 Fase 7 — CI/CD y despliegue
**Objetivo:** Automatizar el flujo de entrega continua y despliegue del sistema.  
**Tareas:**
7.1 Configurar pipelines en GitHub Actions.  
7.2 Pipeline completo (lint + tests + build + deploy).  
7.3 Despliegue en Render / Railway / Vercel.  
7.4 Tests end-to-end automáticos.

---

### 📚 Fase 8 — Documentación profesional y portfolio
**Objetivo:** Entregar la documentación final y preparar el proyecto para el portfolio profesional.  
**Tareas:**
8.1 Redactar documentación arquitectónica final (ADRs, diagramas).  
8.2 Crear resumen “Architecture Summary”.  
8.3 Preparar README final, capturas y video demo.

---

## 🧱 Entregables globales
- Documentación completa en `/docs/`.  
- ADRs justificando cada decisión técnica.  
- Diagramas ERD, de componentes y de despliegue.  
- Backend y frontend funcionales con autenticación.  
- Integración de pagos y notificaciones.  
- Pipeline CI/CD operativo.  
- Demo en producción y documentación profesional.

---

## 🔄 Flujo de trabajo general
Cada **fase** se gestiona mediante una **Issue principal** en GitHub, y dentro de cada Issue se reflejan sus **tareas** mediante una checklist.

Cada **commit** y **PR (Pull Request)** debe incluir el ID de la Issue correspondiente, por ejemplo:

feat: add workshop entity [#2]

fix: adjust payment validation [#5]

