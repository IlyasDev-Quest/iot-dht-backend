# 🌡️/💧 IoT DHT Backend

IoT DHT Backend is a school project designed to process incoming DHT11 sensor readings and expose an API for clients to consume.

---

## Requirements 📋

- [Python](https://www.python.org/downloads/) >= 3.14 🐍
- [Docker](https://www.docker.com/) 🐳
- [Docker Compose](https://docs.docker.com/compose/) ⚙️

---

## Quick Navigation 🔗

- [Project Setup](#project-setup)
- [Development Environment](#development-environment)
- [Deployment Environment (Optional)](#deployment-environment-optional)
- [Project Structure](#project-structure-%F0%9F%97%82%EF%B8%8F)
- [Makefile Commands](#makefile-commands-%E2%9A%A1%EF%B8%8F)
- [Notes](#notes-%F0%9F%93%9D)
- [License](#license-%F0%9F%93%84)

---

## Project Setup 🛠️

### 1. Clone the repository

```bash
git clone https://github.com/IlyasDev-Quest/iot-dht-backend.git
cd iot-dht-backend/app
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows (Git Bash/MinGW):**

```bash
source .venv/Scripts/activate
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Verify the virtual environment

```bash
which python
```

> Ensure the output points to the virtual environment path.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Development Environment 🏗️

### Start the application

```bash
make dev-build
make dev-up
```

### List running containers

```bash
make dev-ps
```

> You should see 3 Docker services running.

> For a full list of Makefile commands, refer to the `Makefile` at the root of the project.

---

## Deployment Environment (Optional) 🚀

### 1. Build the production image

From the `/app` directory:

```bash
docker build . -t your-image-name:image-tag --target prod
```

### 2. Push the image to a registry

```bash
docker tag your-image-name:image-tag some-image-registry/your-image-name:image-tag
docker push some-image-registry/your-image-name:image-tag
```

### 3. Configure deployment environment

Navigate to the `/deploy` directory:

```bash
cd ../deploy
```

Create local environment files:

```bash
cp .env.prod.example .env.prod
cp compose.example.env compose.env
```

Update `.env.prod` with your secrets:

```env
CORS_ORIGINS=
DATABASE_URL=
ENVIRONMENT="prod"
SECRET_KEY=
APP_NAME="IoT DHT Project"
```

(Optional) Update `compose.env` if you want to provide substitute images:

```env
APP_IMAGE="ilyasberkani/iot-dht-backend:0.1"
NGINX_IMAGE="nginx:alpine"
```

### 4. Run the deployment

```bash
make prod-up
```

---

## Project Structure 🗂️

```
iot-dht-backend/
├── .gitignore
├── app/                  # Application source code
│   ├── .dockerignore     # Files ignored by Docker
│   ├── .env.dev          # Dev environment variables
│   ├── alembic.ini       # Alembic DB config
│   ├── api/              # API routes
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── dht11.py
│   │       ├── events.py
│   │       └── user.py
│   ├── core/             # Configs, security, events
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── events.py
│   │   ├── security.py
│   │   └── session/
│   │       ├── __init__.py
│   │       ├── backend.py
│   │       ├── frontend.py
│   │       └── verifier.py
│   ├── db/               # Database connection & seeding
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── seed.py
│   ├── dependencies.py
│   ├── docker-compose.dev.yaml
│   ├── Dockerfile
│   ├── enums/            # Enum definitions
│   ├── main.py
│   ├── migrations/       # Alembic migrations
│   ├── models/           # ORM models
│   ├── nginx.dev.conf
│   ├── repositories/     # Data access layer
│   ├── requirements.txt
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── tests/            # Unit tests
├── deploy/               # Deployment artifacts
│   ├── .env.prod.example
│   ├── compose.env
│   ├── compose.example.env
│   ├── docker-compose.prod.yaml
│   └── nginx.prod.conf
└── Makefile              # Makefile commands for dev/prod
```

---

## Makefile Commands ⚡

### Development

- `make dev-build` - Build dev images
- `make dev-up` - Start dev environment
- `make dev-stop` - Stop containers
- `make dev-down` - Stop and remove containers
- `make dev-logs` - Tail logs
- `make dev-ps` - List running containers

### Production

- `make prod-up` - Start production environment
- `make prod-stop` - Stop containers
- `make prod-down` - Stop and remove containers
- `make prod-logs` - Tail logs
- `make prod-ps` - List running containers

### Database Migrations

- `make dev-migrate` - Run Alembic migrations in dev
- `make prod-migrate` - Run Alembic migrations in prod

---

## Notes 📝

- The project supports both development and production environments via Docker Compose.
- The Makefile simplifies common tasks like starting, stopping, logging, and listing containers.
- Ensure `.env` files contain the correct secrets and configurations before deploying to production.

---

## License 📄

This project is open-source. under the [MIT](https://github.com/IlyasDev-Quest/iot-dht-backend/blob/dev/LICENSE) license.

# 🌡️/💧 IoT DHT Backend

IoT DHT Backend is a school project designed to process incoming DHT11 sensor readings and expose an API for clients to consume.

---

## Requirements 📋

- [Python](https://www.python.org/downloads/) >= 3.14 🐍
- [Docker](https://www.docker.com/) 🐳
- [Docker Compose](https://docs.docker.com/compose/) ⚙️

---

## Quick Navigation 🔗

- [Project Setup](#project-setup)
- [Development Environment](#development-environment)
- [Deployment Environment (Optional)](#deployment-environment-optional)
- [Project Structure](#project-structure-%F0%9F%97%82%EF%B8%8F)
- [Makefile Commands](#makefile-commands-%E2%9A%A1%EF%B8%8F)
- [Notes](#notes-%F0%9F%93%9D)
- [License](#license-%F0%9F%93%84)

---

## Project Setup 🛠️

### 1. Clone the repository

```bash
git clone https://github.com/IlyasDev-Quest/iot-dht-backend.git
cd iot-dht-backend/app
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows (Git Bash/MinGW):**

```bash
source .venv/Scripts/activate
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Verify the virtual environment

```bash
which python
```

> Ensure the output points to the virtual environment path.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Development Environment 🏗️

### Start the application

```bash
make dev-build
make dev-up
```

### List running containers

```bash
make dev-ps
```

> You should see 3 Docker services running.

> For a full list of Makefile commands, refer to the `Makefile` at the root of the project.

---

## Deployment Environment (Optional) 🚀

### 1. Build the production image

From the `/app` directory:

```bash
docker build . -t your-image-name:image-tag --target prod
```

### 2. Push the image to a registry

```bash
docker tag your-image-name:image-tag some-image-registry/your-image-name:image-tag
docker push some-image-registry/your-image-name:image-tag
```

### 3. Configure deployment environment

Navigate to the `/deploy` directory:

```bash
cd ../deploy
```

Create local environment files:

```bash
cp .env.prod.example .env.prod
cp compose.example.env compose.env
```

Update `.env.prod` with your secrets:

```env
CORS_ORIGINS=
DATABASE_URL=
ENVIRONMENT="prod"
SECRET_KEY=
APP_NAME="IoT DHT Project"
```

(Optional) Update `compose.env` if you want to provide substitute images:

```env
APP_IMAGE="ilyasberkani/iot-dht-backend:0.1"
NGINX_IMAGE="nginx:alpine"
```

### 4. Run the deployment

```bash
make prod-up
```

---

## Project Structure 🗂️

```
iot-dht-backend/
├── .gitignore
├── app/                  # Application source code
│   ├── .dockerignore     # Files ignored by Docker
│   ├── .env.dev          # Dev environment variables
│   ├── alembic.ini       # Alembic DB config
│   ├── api/              # API routes
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── dht11.py
│   │       ├── events.py
│   │       └── user.py
│   ├── core/             # Configs, security, events
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── events.py
│   │   ├── security.py
│   │   └── session/
│   │       ├── __init__.py
│   │       ├── backend.py
│   │       ├── frontend.py
│   │       └── verifier.py
│   ├── db/               # Database connection & seeding
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── seed.py
│   ├── dependencies.py
│   ├── docker-compose.dev.yaml
│   ├── Dockerfile
│   ├── enums/            # Enum definitions
│   ├── main.py
│   ├── migrations/       # Alembic migrations
│   ├── models/           # ORM models
│   ├── nginx.dev.conf
│   ├── repositories/     # Data access layer
│   ├── requirements.txt
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── tests/            # Unit tests
├── deploy/               # Deployment artifacts
│   ├── .env.prod.example
│   ├── compose.env
│   ├── compose.example.env
│   ├── docker-compose.prod.yaml
│   └── nginx.prod.conf
└── Makefile              # Makefile commands for dev/prod
```

---

## Makefile Commands ⚡

### Development

- `make dev-build` - Build dev images
- `make dev-up` - Start dev environment
- `make dev-stop` - Stop containers
- `make dev-down` - Stop and remove containers
- `make dev-logs` - Tail logs
- `make dev-ps` - List running containers

### Production

- `make prod-up` - Start production environment
- `make prod-stop` - Stop containers
- `make prod-down` - Stop and remove containers
- `make prod-logs` - Tail logs
- `make prod-ps` - List running containers

### Database Migrations

- `make dev-migrate` - Run Alembic migrations in dev
- `make prod-migrate` - Run Alembic migrations in prod

---

## Notes 📝

- The project supports both development and production environments via Docker Compose.
- The Makefile simplifies common tasks like starting, stopping, logging, and listing containers.
- Ensure `.env` files contain the correct secrets and configurations before deploying to production.

---

## License 📄

This project is open-source. under the [MIT](https://github.com/IlyasDev-Quest/iot-dht-backend/blob/dev/LICENSE) license.
