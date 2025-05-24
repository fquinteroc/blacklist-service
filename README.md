# Microservicio Blacklist

## Ejecución

Para la ejecución local del microservicio y su base de datos, se utiliza `docker compose`. Asegúrese de tener instalado **Docker** y **Docker Compose**.

1. **Clonar este repositorio**:

```bash
git clone https://github.com/fquinteroc/blacklist-service.git
cd blacklist-service
```

2. **Ejecutar docker-compose**:

```bash
docker-compose up --build
```

3. **Verificar contenedores activos**:

```bash
docker ps
```

## Desarrollo

### 1. Crear contenedor

A traves de estas instrucciones se puede construir la imagen del contenedor y crear una instancia de ejecución.

```bash
# docker build: Construye una imagen
# -t: Tag
docker build --build-arg PORT=5005 -t blacklist-service .

# docker images: Lista las imagenes
docker images

# docker run: Ejecuta un contenedor
# -t: TTY
# -d: Detached
# -i: Interactive
# -e: Environment variable
# -v: Volume
# --name: Container name

docker run -td --name blacklist-service blacklist-service

# docker ps: Lista los contenedores
docker ps

# docker exec: Inicializa una consola interactiva en un contenedor
docker exec -ti blacklist-service bash
```

### 2. Correr la imagen

#### 2.1.a. Correr la imagen pasando la llave como variable de entorno

```bash
# Guradar la llave en el archivo .env
docker compose up --build -d
# En desarrollo:
docker compose watch
```

#### 2.1.b. Correr la imagen pasando la llave como variable de entorno

```bash
# the NR license key you retrieved in first section
export NEW_RELIC_LICENSE_KEY=xxxxxxxxxxxx

# run container, pass NR license key as environment variable
docker run -it -p 5005:5005 -e NEW_RELIC_LICENSE_KEY=$NEW_RELIC_LICENSE_KEY --rm --name blacklist-service blacklist-service
```

### 2.2. Ejecutar pruebas de carga sobre el contenedor.

```bash
# Hacer peticiones al api
curl http://localhost:5005

# Hacer peticiones en masa
sudo apt install apache2-utils -y # install Apache Bench
# run 10k tests with 25 concurrent users
ab -n 10000 -c 25 http://localhost:5005/
```

### 2.3. Workflow de desarrollo

```bash
# python3 en linux; py en windows.

# Crear el entorno la primera vez en Linux
python3 -m venv .venv
# Crear el entorno la primera vez en Windows
py -m venv .venv

# Activar el entorno linux
source .venv/bin/activate
# Activar el entorno virtual windows (Git Bash)
source .venv/Scripts/activate


# Trabajar (requiere: Activar el entorno)
# Instala las dependencias en el entorno
pip3 install -r src/requirements.txt
# pip3 install flask
# pip3 install python-dotenv
# pip3 install pytest
# pip3 install sqlalchemy
# pip3 install Werkzeug
# pip3 install psycopg2-binary
# pip3 install gunicorn
# pip3 freeze > requirements.txt

# Ejecuta la aplicación
FLASK_APP=application.py flask run

# Desactivar el entorno (requiere: Activar el entorno)
deactivate
```

## Ejemplos de Llamada al micorservicio

### 1. Ping

```bash
export SECRET_TOKEN_BLACKLIST='secret_token_blacklist'
```

```bash
curl --location 'http://localhost:5006/ping'
```

### 2. Agregar un email a la lista negra global de la organización.

```bash
curl --location 'http://localhost:5006/blacklists' \
--header 'Content-Type: application/json' \
--header "Authorization: ${SECRET_TOKEN_BLACKLIST}" \
--data-raw '{
    "email": "curl@example.com",
    "app_uuid": "123c4567-c89b-12b3-c456-426614174000",
    "blocked_reason": "Test manual con curl"
}'
```

### 3. Saber si un email está en la lista negra global de la organización o no, y el motivo por el que fue agregado a la lista negra.

```bash
curl --location 'http://localhost:5006/blacklists/postman@example.com' \
--header "Authorization: ${SECRET_TOKEN_BLACKLIST}"
```
