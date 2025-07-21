# 🧳 QUITOGONEW – Sistema Distribuido para Gestión de Paquetes Turísticos

Este proyecto implementa una arquitectura de microservicios en Flask para gestionar usuarios, paquetes turísticos y reservas, con seguridad mediante JWT, registro en Consul y despliegue en contenedores Docker.

---

## 🚀 Servicios Principales

### 🛡️ Auth Service (`auth-service`)
Autenticación y autorización de usuarios (JWT).

- **Tecnología**: Flask + PostgreSQL
- **Puerto**: `5000`
- **Base URL**: `http://localhost:5000`

| Método | Endpoint    | Requiere Token | Descripción                                      |
|--------|-------------|----------------|--------------------------------------------------|
| POST   | `/register` | ❌ No          | Registrar nuevo usuario (email, password, rol)  |
| POST   | `/login`    | ❌ No          | Iniciar sesión, devuelve token JWT              |
| GET    | `/me`       | ✅ Sí          | Retorna datos del usuario autenticado           |
| GET    | `/health`   | ❌ No          | Verifica la salud del servicio                  |

---

### 📦 Package Service (`package-service`)
Gestión de paquetes turísticos.

- **Tecnología**: Flask + PostgreSQL
- **Puerto**: `5001`
- **Base URL**: `http://localhost:5001`

| Método | Endpoint              | Requiere Token | Rol        | Descripción                                |
|--------|------------------------|----------------|------------|--------------------------------------------|
| GET    | `/packages/public`     | ❌ No          | —          | Lista pública de paquetes turísticos       |
| GET    | `/packages`            | ✅ Sí          | user/admin | Lista completa de paquetes                 |
| POST   | `/packages`            | ✅ Sí          | admin      | Crear nuevo paquete                        |
| PUT    | `/packages/<id>`       | ✅ Sí          | admin      | Actualizar paquete por ID                  |
| DELETE | `/packages/<id>`       | ✅ Sí          | admin      | Eliminar paquete por ID                    |
| GET    | `/health`              | ❌ No          | —          | Verifica la salud del servicio             |

---

### 📅 Booking Service (`booking-service`)
Gestión de reservas de paquetes turísticos.

- **Tecnología**: Flask + MongoDB
- **Puerto**: `5002`
- **Base URL**: `http://localhost:5002`

| Método | Endpoint              | Requiere Token | Rol   | Descripción                                         |
|--------|------------------------|----------------|-------|-----------------------------------------------------|
| POST   | `/bookings`            | ✅ Sí          | user  | Crear nueva reserva (package_id, travel_date)       |
| GET    | `/bookings`            | ✅ Sí          | user  | Listar reservas del usuario actual                  |
| DELETE | `/bookings/<id>`       | ✅ Sí          | user  | Cancelar reserva por ID                             |
| GET    | `/bookings/report`     | ✅ Sí          | admin | Reporte de reservas entre fechas (start, end)       |
| GET    | `/health`              | ❌ No          | —     | Verifica la salud del servicio                      |

---

## 🔐 Seguridad

- Todos los servicios usan autenticación **JWT**
- Validación de rol (`admin` o `user`) a través del endpoint `/me` de `auth-service`
- Descubrimiento de servicios mediante **Consul**

---

## 🧩 Arquitectura

- **Estilo**: Microservicios REST
- **Lenguaje**: Python (Flask)
- **BDs**: PostgreSQL (`auth`, `package`), MongoDB (`booking`)
- **Comunicación entre servicios**: HTTP + JWT + Service Discovery
- **Orquestación**: Docker + Docker Compose