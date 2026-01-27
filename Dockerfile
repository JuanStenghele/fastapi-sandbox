FROM python:3.10

WORKDIR /fastapi-sandbox

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r /fastapi-sandbox/requirements.txt

# DB migrations files
COPY ./alembic.ini ./
COPY ./alembic ./alembic

COPY ./src ./src

CMD ["fastapi", "dev", "/fastapi-sandbox/src/main.py", "--port", "8000", "--host", "0.0.0.0"]
