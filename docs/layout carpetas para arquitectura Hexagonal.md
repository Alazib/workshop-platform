# 📁 Estructura completa del backend
## Arquitectura Hexagonal + Django

```text
backend/
├── Pipfile
├── Pipfile.lock
├── manage.py
│
├── config/                         # 0 · Proyecto Django (configuración del framework para la infrastructura)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── domain/                         # 1 · NÚCLEO DEL DOMINIO (reglas de negocio puras)
│   ├── __init__.py
│   ├── entities/                   # Entidades del dominio
│   │   └── __init__.py
│   ├── value_objects/              # Value Objects (Email, Money, DateRange…)
│   │   └── __init__.py
│   ├── services/                   # Servicios de dominio (políticas, reglas)
│   │   └── __init__.py
│   └── ports/                      # Interfaces hacia la infraestructura
│       └── __init__.py
│
├── application/                    # 2 · CAPA DE APLICACIÓN (casos de uso)
│   ├── __init__.py
│   └── use_cases/                  # RegisterToSession, ConfirmPayment…
│       └── __init__.py
│
└── infrastructure/                 # 3 · INFRAESTRUCTURA (Django, ORM, APIs, repos)
    ├── __init__.py
    └── django_app/                 # App Django como adaptador HTTP / ORM
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── views.py
        ├── urls.py                 # (si se necesita)
        ├── serializers.py          # (si se necesita)
        ├── repositories.py         # Implementaciones de los puertos
        ├── api/                    # Endpoints REST organizados por slice
        │   ├── __init__.py
        │   └── (ficheros de endpoints por slice)
        └── migrations/
            └── __init__.py
