# 📦 Package Service

Este microservicio forma parte del sistema distribuido para la gestión de paquetes turísticos. Está desarrollado con **Flask**, utiliza **PostgreSQL** como base de datos, y aplica una arquitectura limpia con **DTO**, **DAO**, **Abstract Factory** y descubrimiento de servicios mediante **Consul**.

---

## 🚀 Tecnologías

* **Lenguaje**: Python 3.11
* **Framework**: Flask
* **Base de datos**: PostgreSQL
* **Service Registry**: Consul
* **Contenedores**: Docker, Docker Compose
* **Autenticación**: JWT (validados contra `auth-service`)

---

## 📁 Estructura del Proyecto

```
package-service/
├── app/
│   ├── auth/                     # Middleware de autenticación y roles
│   ├── controllers/              # Endpoints (controladores Flask)
│   ├── db/                       # Conexión a PostgreSQL
│   ├── dto/                      # Data Transfer Objects
│   ├── factories/                # Abstract Factory para DAOs
│   ├── repositories/             # Interfaces y DAOs concretos
│   └── services/                 # Lógica de negocio
├── consul_register.py           # Registro automático en Consul
├── Dockerfile                   # Imagen del microservicio
├── docker-compose.yml           # Orquestación de servicios
├── init-scripts/init.sql        # Inicializa DB packages_db
├── .env.example                 # Variables de entorno de ejemplo
├── .gitignore
├── main.py                      # Punto de entrada
└── requirements.txt
```

---

## ⚙️ Variables de Entorno

Copia `.env.example` como `.env` y modifica los valores necesarios:

```env
PG_HOST=postgres
PG_PORT=5432
PG_DATABASE=packages_db
PG_USER=postgres
PG_PASSWORD=postgres123

CONSUL_HOST=consul
CONSUL_PORT=8500

SERVICE_NAME=package-service
SERVICE_ID=package-service-1
SERVICE_HOST=0.0.0.0
SERVICE_PORT=5002

FLASK_DEBUG=false
```

---

## 🐳 Docker Compose

Este microservicio puede levantarse junto con PostgreSQL, Consul y demás servicios:

```bash
docker compose up --build
```

Incluye healthchecks y dependencias para asegurar que los servicios inicien en orden correcto.

---

## 🔐 Seguridad y JWT

Cada petición a endpoints protegidos requiere un JWT en el header `Authorization`. Este token es validado llamando al endpoint `/me` del `auth-service` mediante Consul (sin hardcodear IP).

```http
GET /packages HTTP/1.1
Authorization: Bearer <jwt_token>
```

---

## 📌 Endpoints

| Método | Endpoint       | Autenticación | Rol requerido |
| ------ | -------------- | ------------- | ------------- |
| GET    | /packages      | ✅ JWT         | admin         |
| POST   | /packages      | ✅ JWT         | admin         |
| PUT    | /packages/<id> | ✅ JWT         | admin         |
| DELETE | /packages/<id> | ✅ JWT         | admin         |
| GET    | /health        | ❌ No          | -             |

---

## ✅ Verificación de estado

Revisa el estado del microservicio con:

```bash
curl http://localhost:5002/health
```

Respuesta:

```json
{ "status": "ok" }
```

---

## 🧪 Pruebas

Puedes agregar pruebas funcionales usando `pytest` o `unittest` dentro del directorio `tests/`.

---

## 📦 Construcción manual con Docker

```bash
docker build -t package-service .
docker run -p 5002:5002 --env-file .env package-service
```

---

## 🧠 Notas adicionales

* El microservicio se registra automáticamente en Consul al iniciarse.
* Puedes consultar su estado desde la UI de Consul: `http://localhost:8500`
* Usa el archivo `init.sql` para crear `packages_db` si no existe.

---

## ✍ Autor

Desarrollado por \[Tu Nombre] para el sistema distribuido de gestión de paquetes turísticos.

---

© 2025 - Todos los derechos reservados.
