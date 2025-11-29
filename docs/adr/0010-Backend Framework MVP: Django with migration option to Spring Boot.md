# ADR 0010 — Framework backend para el MVP. Django con opción de migración a Spring Boot

- Estado: ACEPTADA
- Fecha: 2025-11-18
- Contexto: Selección de framework backend para el MVP de Workshop Platform

## 1. Contexto

En la Fase 2 queremos implementar un **MVP funcional** del backend que permita:

- Ver sesiones publicadas.
- Inscribir usuarios.
- Registrar pagos simulados.
- Confirmar/cancelar inscripciones.
- Listar inscripciones para administradores.

Condicionantes importantes:

- El proyecto es también una pieza de **portfolio**:
  - Debe demostrar arquitectura sólida (hexagonal).
  - Debe ser legible y razonablemente profesional.
- Necesitamos avanzar relativamente rápido:
  - El tiempo/capacidad de desarrollo es limitado.
  - No podemos malgastar semanas luchando contra configuración compleja.
- A medio plazo, queremos dejar abierta la opción de:
  - Migrar a **Spring Boot** como ejercicio arquitectónico.
  - Mostrar que el dominio es independiente del framework.

Por tanto, el framework elegido para el MVP debe:

- Permitir desarrollar rápido.
- Disponer de un ecosistema maduro (ORM, migraciones, tests).
- Integrarse bien con una arquitectura hexagonal.
- No “secuestrar” el dominio.

## 2. Decisión

Para el **MVP inicial**, elegimos:

- Backend implementado con **Django** (Python).
- Arquitectura hexagonal para desacoplar dominio y framework.
- Documentar un **plan de migración futura a Spring Boot** en un ADR separado o en este mismo como sección.

En resumen:

- **MVP = Django + Hexagonal**
- **Evolución posible = Spring Boot reutilizando dominio y casos de uso (reescribiendo solo adaptadores)**

## 3. Argumentos a favor de Django para el MVP

### 3.1. Rapidez de desarrollo

Django aporta:

- ORM integrado.
- Sistema de migraciones.
- Administración básica (aunque no sea prioridad).
- Mecanismos sencillos para exponer endpoints (views, DRF si se necesitara).

Esto nos permite:

- Centrarnos en el dominio y en la arquitectura, no en la configuración.
- Tener algo demostrable (API funcional) en menos tiempo.

### 3.2. Complejidad razonable para un solo desarrollador

Spring Boot, aunque muy poderoso, exige:

- Más configuración inicial (build, dependencias, estructura).
- Entender bien el ecosistema Java (Spring Data, seguridad, etc.).

Django, en cambio:

- Es más accesible para prototipado.
- Permite equivocarnos barato y refactorizar luego manteniendo el dominio aislado.

### 3.3. Buen encaje con Arquitectura Hexagonal

Aunque Django por defecto empuja a un enfoque MVC clásico, podemos:

- Ubicar las views y modelos ORM dentro de `infrastructure/`.
- Mantener el dominio en módulos Python “puros”, sin referencia a Django.
- Crear interfaces (puertos) que Django implementa como adaptadores.

De esta forma, Django es solo “el framework de infraestructura”, no la base del dominio.

## 4. Alternativas consideradas

### 4.1. Opción A — Spring Boot como framework principal desde el inicio

**Ventajas:**

- Muy valorado en mercado (empresas Java).
- Ecosistema robusto (Spring Data, Spring Security, etc.).
- Perfecto para proyectos grandes y complejos.

**Por qué NO la elegimos para el MVP:**

- Mayor curva de entrada y de configuración inicial.
- Probabilidad más alta de “atascarse” en detalles técnicos (configuración Maven/Gradle, etc.).
- Ralentiza la obtención de un MVP funcional:
  - El objetivo ahora es tener “algo que funciona” + arquitectura clara.
- Aunque es una gran opción a medio/largo plazo, para este proyecto preferimos:
  - Empezar rápido.
  - Demostrar la arquitectura.
  - Evaluar luego el esfuerzo de migración.

### 4.2. Opción B — Node/TypeScript (NestJS u otro framework)

**Ventajas:**

- Muy popular y moderno.
- Buen encaje con frontend si se usa TypeScript en ambos lados.
- NestJS aporta una estructura modular potente (similar a Angular/Spring).

**Por qué NO la elegimos:**

- Añadiría otra pila tecnológica más al proyecto (ya tenemos Python, posiblemente Java, y TS en frontend).
- El objetivo no es explorar todos los stacks posibles, sino mostrar:
  - Buen dominio.
  - Buena arquitectura.
  - Una migración bien pensada entre dos stacks (Django ↔ Spring Boot).

### 4.3. Opción C — Django pero sin arquitectura hexagonal (Django clásico)

**Ventajas:**

- Aún más rápido al principio.
- Menos “ceremonia”: todo son modelos, views y forms.

**Por qué NO la elegimos:**

- El dominio quedaría mezclado con los modelos del ORM y las views.
- Difícil mostrar una arquitectura limpia y desacoplada en el portfolio.
- Mucho más costoso migrar después a Spring Boot (habría que “desenmarañar” el dominio del framework).
- Los tests dependerían de Django para casi todo.

La combinación Django + Hexagonal nos da:

- Velocidad inicial.
- Un dominio protegido del framework.
- Un buen relato arquitectónico (MVP rápido + migración posible).

## 5. Plan de migración futura a Spring Boot (visión general)

Gracias a la arquitectura hexagonal:

- El dominio vive en módulos Python puros.
- Los casos de uso (application layer) también son Python puro.
- Django solo aparece en `infrastructure/` (repositorios, controladores, configuración).

Para migrar a Spring Boot, la idea sería:

1. **Reimplementar el dominio en Java/Kotlin**, respetando:
   - Entidades.
   - Value objects.
   - Máquinas de estado.
   - Interfaces de puertos (repositorios, servicios externos).

2. **Reimplementar los casos de uso** en la capa de aplicación de Spring:
   - Misma lógica.
   - Mismos flujos.
   - Mismos puertos.

3. **Crear nuevos adaptadores en Spring Boot**:
   - Repositorios con Spring Data / JPA.
   - Controladores REST.
   - Integraciones externas.

4. Mantener la misma semántica de los endpoints:
   - Para que la API pública sea lo más compatible posible.

La clave es que, gracias a este ADR y al ADR 0009 (Arquitectura Hexagonal):

- Sabemos que el dominio no debería depender de detalles concretos de Django.
- El ejercicio de migración se convierte en:
  - “Reescribir en otro lenguaje los mismos casos de uso y dominio”.
  - No en “intentar arrancar medio Django dentro de Spring”.

## 6. Consecuencias

### 6.1. Positivas

- MVP más rápido y enfocado en el dominio.
- Menos fricción inicial para construir las primeras vertical slices.
- El código será un buen ejemplo de:
  - Arquitectura hexagonal.
  - Dominio desacoplado.
  - Evolución posible del stack tecnológico.
- Posibilidad real de usar la futura migración como:
  - Capítulo adicional de portfolio.
  - Ejercicio personal de arquitectura y refactorización.

### 6.2. Negativas / Trade-offs

- Parte del trabajo se hará dos veces si finalmente se migra a Spring Boot:
  - Reescritura del dominio y casos de uso en Java/Kotlin.
- El proyecto tendrá, a lo largo de su vida, múltiples lenguajes:
  - Python (Django).
  - TypeScript (frontend).
  - Potencialmente Java/Kotlin (Spring Boot).

Aceptamos este coste porque:

- El objetivo educativo/portfolio lo justifica.
- La arquitectura hexagonal minimiza el impacto de la migración.
- El MVP rápido tiene prioridad sobre la “elegancia perfecta” de elegir Spring Boot desde el día 1.

## 7. Pasos concretos a realizar tras este ADR

1. Crear el proyecto backend con Django.
2. Configurar la estructura de carpetas:
   - `domain/`
   - `application/`
   - `infrastructure/`
3. Implementar el primer slice vertical:
   - RegisterToSessionUseCase + endpoint POST de inscripción.
4. Añadir documentación en `/docs/` explicando:
   - Que el MVP se basa en Django.
   - Que la arquitectura hexagonal permite la futura migración a Spring Boot.
5. Revisar periódicamente el código para garantizar que:
   - Ninguna regla de negocio se filtra a modelos Django o controladores.
