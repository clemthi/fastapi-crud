# City score web-api

Basic REST API with CRUD endpoints using the FastAPI framework.

- [1. Features](#1-features)
- [2. Init dev environement](#2-init-dev-environement)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Create virtual environment](#22-create-virtual-environment)
  - [2.3. Activate virtual environment](#23-activate-virtual-environment)
    - [2.3.1. Linux](#231-linux)
    - [2.3.2. Windows](#232-windows)
  - [2.4. Install requirements](#24-install-requirements)
  - [2.5. Start project](#25-start-project)
    - [2.5.1. Configuration settings](#251-configuration-settings)
    - [2.5.2. Database init](#252-database-init)
    - [2.5.3. Start web server](#253-start-web-server)
- [3. Docker](#3-docker)
  - [3.1. Build docker image](#31-build-docker-image)
  - [3.2. Run local Docker-compose](#32-run-local-docker-compose)
- [4. App configuration](#4-app-configuration)
- [5. Test](#5-test)
- [6. Database migration](#6-database-migration)

## 1. Features

- FastAPI framework
- Asynchronous endpoint
- PostgreSQL as database (SQLite can be used for local dev-env)
- SQLAlchemy as ORM
- Alembic for database schema migration
- Keycloack for access control
- Docker image
- Docker-compose for local dev
- Pytest for unit tests

## 2. Init dev environement

### 2.1. Requirements

- Python 3.8+
- PostgreSQL database

Basic configuration for VSCode (launchers, settings and linter task) is also included in the `./vscode` folder.

### 2.2. Create virtual environment

```bash
cd /path/to/project
python -m venv .venv
```

### 2.3. Activate virtual environment

#### 2.3.1. Linux

```bash
source .venv/bin/activate
```

#### 2.3.2. Windows

```shell
\.venv\Scripts\activate.bat
```

### 2.4. Install requirements

```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 2.5. Start project

#### 2.5.1. Configuration settings

Create an `.env` file in the project root folder file to set the database parameters (see the `app.core.config.Settings` class for the variable list).

The conf to run allong side with the docker-compose stack (see below) is the following:

```ini
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
CREATE_DATASET=True
KEYCLOACK_URL=http://127.0.0.1:8081/auth/
KEYCLOACK_REALM=cityscore
KEYCLOACK_CLIENT_ID=back
KEYCLOACK_ADMIN_ROLE=api_admin
```

You can also add CORS allowed origins with you want to run API along side a front-end client.

```ini
ALLOWED_ORIGINS=["http://localhost:4200"]
```

#### 2.5.2. Database init

Run the database initialization with :

```bash
./upgrade_db.sh
```

This script executes the 2 following steps :

- Database schema initiallization with alembic : `alembic upgrade head`
- Creation of the initial dataset (currently dummy data) : `alembic upgrade head`

#### 2.5.3. Start web server

Then start the service with:

```bash
uvicorn app.main:app
```

And you can check the OpenAPI UI on [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 3. Docker

To build the image of this project you need [BuildKit to be enabled](https://docs.docker.com/develop/develop-images/build_enhancements/#to-enable-buildkit-builds).

### 3.1. Build docker image

The Docker image of the project can be built locally with the following command:

```bash
docker build -t cityscore/webapi:local .
```

### 3.2. Run local Docker-compose

A docker-compose configuration can be found in `docker/docker-compose.yml` and contains everything to run the back-end locally. You can start the docker-compose stack the following command:

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Once started 3 containers are running:

- A Keycloack server for authentication, accessible on [http://127.0.0.1:8081](http://127.0.0.1:8081). it starts with a realm and a set of test users (see `docker/keycloack/realm-export.json`).
- A PostgreSQL database server, accessible on the port **5432**.
- The backend server, accessible on [http://127.0.0.1:8080](http://127.0.0.1:8080/docs).

## 4. App configuration

The configuration of the back-end is done through the environment variables:

| Variable             | Description                                                                    | Mandatory | Default value | Example                                                                           |
| -------------------- | ------------------------------------------------------------------------------ | --------- | ------------- | --------------------------------------------------------------------------------- |
| API_V1_STR           | root path of the APIs                                                          | x         | `/api/v1`     | `/v1` ; `/`                                                                       |
| ALLOWED_ORIGINS      | [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) allowed origins |           |               | `["http://localhost:4200"]` ; `["http://localhost:4200","http://localhost:4201"]` |
| POSTGRES_SERVER      | url of the database server                                                     | x         |               |                                                                                   |
| POSTGRES_PORT        | port of the database server                                                    | x         |               |                                                                                   |
| POSTGRES_USER        | database username                                                              | x         |               |                                                                                   |
| POSTGRES_PASSWORD    | database password                                                              | x         |               |                                                                                   |
| POSTGRES_DB          | postgresql database                                                            | x         |               |                                                                                   |
| KEYCLOACK_URL        | Keycloack authentication server URL                                            | x         |               | `https://sso.example.com/auth/`                                                   |
| KEYCLOACK_REALM      | Keycloack realm                                                                | x         |               |                                                                                   |
| KEYCLOACK_CLIENT_ID  | Keycloack client                                                               | x         |               |                                                                                   |
| KEYCLOACK_ADMIN_ROLE | Keycloack role allowed to use creation/update/deletion endpoints               | x         |               | `admin` ; `api-admin`                                                             |
| USE_SQLITE           | **For local use ONLY** Flag to use a SQLite file instead of a PostgreSQL data. |           | `False`       |                                                                                   |
| CREATE_DATASET       | Insert data on application start. For the moment it's a set of dummy data.     |           | `False`       |                                                                                   |

## 5. Test

Pytest is the project's test framework and Tests are implemented in the `app/tests` folder.

Default options are set in the `pytest.ini` file, so you simply need to execute the `pytest` command to run them.

## 6. Database migration

To modify the database structure just follow these steps:

1. modify and/or add new db models (`app/models/`)
2. run alembic to auto generate the revision :

```bash
alembic revision --autogenerate -m "stuff modified"
```

3. review the revision script in `alembic/versions/`
4. run the upgrade :

```bash
alembic upgrade head
```
