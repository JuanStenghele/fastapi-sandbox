FROM python:3.10

WORKDIR /fastapi-sandbox

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r /fastapi-sandbox/requirements.txt

# Install PostgreSQL client for DB migrations
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# DB migrations files
COPY ./alembic.ini ./
COPY ./alembic ./alembic

COPY ./scripts ./scripts

COPY ./src ./src

CMD ["fastapi", "dev", "/fastapi-sandbox/src/main.py", "--port", "8000", "--host", "0.0.0.0"]
