# ADR 0009 — Arquitectura Hexagonal (Ports & Adapters)

- Estado: ACEPTADA
- Fecha: 2025-11-18
- Contexto: Fase 2 — Diseño de la arquitectura backend para Workshop Platform

## 1. Contexto

Workshop Platform es una aplicación orientada a dominio, con reglas de negocio relativamente ricas:

- Inscripciones con estados (`reserved`, `confirmed`, `attended`, etc.).
- Gestión de aforos.
- Política de cancelación (regla de 7 días).
- Modelo de pagos y reembolsos (`charge` / `refund`).

Además:

- El proyecto debe servir como pieza de portfolio profesional.
- Queremos empezar el MVP con un stack, pero dejando abierta la opción de migrar a otro (por ejemplo, de Django a Spring Boot).
- Necesitamos poder testear el dominio sin depender del framework, ni de la base de datos, ni de la API HTTP.

Los riesgos si ligamos la lógica al framework:

- Cualquier cambio de framework (Django → Spring Boot) obliga a reescribir gran parte de la lógica.
- Los modelos del ORM se acaban llenando de reglas de negocio.
- Los tests se vuelven lentos y frágiles (necesitan levantar framework, DB, etc.).
- Dificultad para razonar sobre el dominio porque está disperso.

Por estos motivos, necesitamos una arquitectura que:

1. Proteja el dominio del resto de la infraestructura.
2. Permita intercambiar adaptadores (API HTTP, DB, pasarela de pagos).
3. Facilite el TDD y los tests de dominio puros.
4. Sea legible como ejemplo de “arquitectura limpia” en un portfolio.

## 2. Decisión

Adoptamos **Arquitectura Hexagonal (Ports & Adapters)** como estilo principal del backend.

### 2.1. Estructura general

Organizaremos el código en tres grandes capas lógicas:

- `domain/`
  - Entidades, value objects, máquinas de estado.
  - Servicios de dominio (invariantes, lógica compleja).
  - Interfaces (puertos) para acceder a recursos externos:
    - Repositorios (SessionRepository, RegistrationRepository, PaymentRepository…).
    - Servicios externos (PaymentGateway, EmailService…).

- `application/`
  - Casos de uso (application services), e.g.:
    - RegisterToSessionUseCase
    - ConfirmPaymentForRegistrationUseCase
    - CancelRegistrationByUserUseCase
    - CancelRegistrationByOrganizerUseCase
    - ListSessionRegistrationsUseCase
  - Orquestan llamadas al dominio y a los puertos.
  - No conocen detalles del framework ni del ORM.

- `infrastructure/`
  - Implementaciones concretas de los puertos (adaptadores):
    - Repositorios basados en Django ORM (o el que toque).
    - Adaptadores a sistemas externos (pasarelas de pago, email).
  - Controladores / views (API HTTP).
  - Configuración específica del framework.

### 2.2. Principio clave

El dominio no importa ninguna clase de infraestructura.

- Dominio → solo ve interfaces (puertos).
- Infraestructura → implementa esas interfaces (adaptadores).

Ejemplo conceptual:

- Puerto en `domain/`:
    interface RegistrationRepository
        save(registration)
        findById(id)
        findBySessionId(sessionId)

- Adaptador en `infrastructure/`:
    DjangoRegistrationRepository implements RegistrationRepository

El caso de uso `RegisterToSessionUseCase`:

- Recibe un DTO.
- Valida la lógica de negocio (sesión publicada, aforo, usuario no duplicado).
- Llama a `RegistrationRepository` (sin saber que detrás hay Django, SQLite, PostgreSQL o un repositorio en memoria).

## 3. Alternativas consideradas

### 3.1. Arquitectura por capas “clásica” (Controllers → Services → Repositories)

**Descripción rápida:**

- Controladores (HTTP) llaman a servicios.
- Servicios llaman a repositorios.
- Repositorios usan el ORM.

**Por qué NO la elegimos como enfoque principal:**

- Aunque separa algo las responsabilidades, en la práctica suele derivar en:
  - Servicios demasiado grandes y muy acoplados al framework.
  - Dominio mezclado con lógica de infraestructura (p. ej. modelos de Django llenos de lógica de negocio).
- Cambiar de framework (Django → Spring Boot) implica rehacer gran parte de los services y modelos.
- Menor claridad a la hora de mostrar el dominio como “núcleo independiente” en un portfolio.

### 3.2. Clean Architecture “pura” (con más capas y círculos)

**Ventajas:**

- Aún más explícita en la separación de capas.
- Filosofía similar a Hexagonal (dominio en el centro).

**Por qué NO la elegimos explícitamente:**

- Para el tamaño del proyecto, puede resultar demasiado ceremoniosa:
  - Más capas.
  - Más interfaces.
  - Más complejidad conceptual.
- Arquitectura hexagonal ya proporciona separación de dominio e infraestructura de forma suficiente y más pragmática.
- Hexagonal es más fácil de explicar y visualizar en un ADR y en el código.

En la práctica, nuestro enfoque será muy cercano a “Clean Architecture”, pero adoptando el vocabulario y la simplicidad de **Ports & Adapters (Hexagonal)**.

## 4. Consecuencias

### 4.1. Positivas

- El dominio será independiente de Django, Spring Boot o cualquier otro framework.
- Podremos:
  - Empezar el MVP en Django.
  - Diseñar un camino realista de migración a Spring Boot sin tocar el dominio.
- Tests de dominio rápidos y puros:
  - Usando repositorios en memoria.
  - Sin levantar servidor HTTP, ni DB, ni framework.
- Mejor calidad del código como pieza de portfolio:
  - Se verá claramente la intención de arquitectura.
  - El dominio quedará documentado y legible.

### 4.2. Negativas / Trade-offs

- Aumenta la cantidad de ficheros y “ceremonia” (más interfaces, más clases).
- Curva de aprendizaje:
  - Requiere disciplina para no “colarse” lógica de negocio en las capas de infraestructura.
- Para un MVP muy pequeño, podría parecer “overkill”; sin embargo, en este caso lo aceptamos porque:
  - El objetivo del proyecto es también formativo y de portfolio.
  - La complejidad de dominio justifica esta inversión.

## 5. Implementación inicial

- Crear los directorios `domain/`, `application/`, `infrastructure/` en el backend.
- Definir puertos (interfaces) de repositorios y servicios externos en `domain/`.
- Implementar el primer caso de uso (RegisterToSessionUseCase) como primer vertical slice:
  - Dominio → entidades y puertos.
  - Application → caso de uso.
  - Infrastructure → adaptadores (repos Django + controlador HTTP).
- Ir ampliando el resto de casos de uso respetando esta separación.
