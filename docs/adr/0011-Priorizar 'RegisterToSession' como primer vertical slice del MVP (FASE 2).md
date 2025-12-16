# ADR 0011 — Priorizar `RegisterToSession` como primer vertical slice del MVP (FASE 2)

## Estado
Aceptado

## Contexto

En la FASE 2 queremos construir un **MVP funcional del backend** con **Django** como infraestructura y **arquitectura hexagonal** (dominio y aplicación desacoplados de Django/ORM).
El MVP de ensure incluye el flujo de negocio principal:

- Inscripción a sesión
- Pago simulado
- Confirmación tras pago
- Cancelaciones
- Listado de inscripciones

Surge la duda: ¿por qué empezar el desarrollo por el caso de uso **RegisterToSession** (inscripción) y no por **CreateSession** (crear sesión)?

## Decisión

Empezamos la FASE 2 por el slice **RegisterToSession** en lugar de **CreateSession**.

## Justificación

### 1) El MVP está definido por el “core flow” del producto, no por CRUD
El MVP de esta fase se valida si el sistema soporta el flujo completo:

Inscripción → Pago (simulado) → Confirmación → Cancelación → Listado

Este flujo es la parte de mayor valor funcional (lo que “hace” el producto).
En comparación, `CreateSession` es un CRUD/backoffice que, aunque necesario, no valida el core flow.

### 2) Django Admin permite crear sesiones sin construir todavía el caso de uso `CreateSession`
Django Admin ya nos ofrece un panel “backoffice” para:

- Crear sesiones (`SessionModel`)
- Editarlas
- Cambiar estados manualmente (temporalmente, durante MVP)

Esto permite desbloquear el desarrollo del core flow sin invertir tiempo inicial en endpoints CRUD que no aportan valor de negocio inmediato.

### 3) `RegisterToSession` obliga a implementar la arquitectura hexagonal “de verdad”
`RegisterToSession` fuerza a construir las piezas clave del enfoque hexagonal:

- Puertos (interfaces repositorio) en `domain/ports`
- Caso de uso en `application/use_cases`
- Errores de dominio y manejo consistente
- Repositorios in-memory para tests unitarios sin Django
- Implementación de repositorios Django como adaptadores reales
- Un endpoint HTTP que use el caso de uso y traduzca errores a respuestas

Es un slice con suficiente “profundidad técnica” como para demostrar que la arquitectura está funcionando.

En cambio, `CreateSession` suele ser demasiado cercano a un CRUD directo:
- Es fácil caer en “Django clásico” (views → ORM directo) y posponer la hexagonalidad real.
- Se aprende menos sobre puertos/adaptadores y reglas.

### 4) `CreateSession` depende de decisiones y dependencias que suelen llegar después
Crear sesiones de forma robusta suele implicar responder preguntas del dominio y del producto:

- ¿Quién puede crear sesiones? (auth/roles)
- ¿En qué estado nacen? (draft/announced)
- ¿Cómo se validan fechas? (starts_at < ends_at, etc.)
- ¿Qué relación tiene con Workshop/Venue/Organizers?
- ¿Se permite crear published directamente o hay transiciones obligatorias?

Empezar por `RegisterToSession` permite avanzar sin abrir todavía ese árbol de decisiones.

### 5) Alineación con el plan de slices del MVP (FASE 2)
El plan original de FASE 2 prioriza:
- Inscripción
- Pago
- Confirmación
- Cancelaciones
- Listado

Por tanto, iniciar por `RegisterToSession` mantiene coherencia con los criterios de aceptación del MVP.

## Alternativas consideradas

### Alternativa A — Empezar por `CreateSessionUseCase`
Pros:
- El orden conceptual parece más natural (“primero creo sesiones, luego me inscribo”).
- Se diseña antes el ciclo de vida de Session.

Contras:
- Alto riesgo de convertir el primer slice en un CRUD sin profundidad (no se prueba el core flow).
- Bloquea por decisiones de auth/roles y modelado extra (workshops, ownership, etc.).
- Retrasa la implementación de la arquitectura hexagonal “completa” (puertos, adaptadores, errores, endpoint).

### Alternativa B — Hacer ambos en paralelo
Pros:
- Se avanza en backoffice y en core flow.

Contras:
- Aumenta complejidad inicial y dispersa el aprendizaje.
- Incrementa probabilidad de inconsistencias de diseño y refactors tempranos.

## Consecuencias

- El MVP se apoya inicialmente en Django Admin como backoffice para crear sesiones.
- El core flow (`RegisterToSession`) se implementa end-to-end primero, validando arquitectura y patrones.
- `CreateSession` se pospone para una fase posterior (p.ej., Fase 3), cuando:
  - haya autenticación mínima,
  - y haya claridad en ciclo de vida y permisos.
- Se reconoce una deuda técnica explícita:
  - “Endurecer Admin para no saltarse reglas del dominio” (planeado como slice posterior).
