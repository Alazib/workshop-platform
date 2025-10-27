# ADR 0001: Elección inicial de stack

## Contexto
El proyecto consiste en una plataforma para la gestión de talleres y eventos culturales, con funcionalidades de inscripción, pagos y dashboards básicos para administradores y organizadores.

## Decisión
Trabajaremos de forma **tecnología-agnóstica en la fase de modelado**. Posteriormente se evaluará si conviene:
- **Django (Python):** prototipado rápido, admin panel, ORM integrado, integraciones fáciles con pasarelas de pago.
- **Spring Boot (Java):** enfoque empresarial, arquitectura más compleja, más valorado en ciertos entornos profesionales.

Para el MVP inicial se recomienda Django, con la opción de documentar una posible migración a Spring Boot como ejercicio arquitectónico.

## Estado
Aceptada.

## Consecuencias
- Nos permite avanzar en el modelado sin bloquear por la tecnología.
- Ganamos flexibilidad: un MVP rápido en Django puede servir de demo, mientras que una justificación/migración a Spring Boot aporta valor curricular y arquitectónico.
