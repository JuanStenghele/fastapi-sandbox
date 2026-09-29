FROM python:3.13

# Add Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 /lambda-adapter /opt/extensions/lambda-adapter

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

RUN chmod +x /fastapi-sandbox/scripts/run_server.sh
CMD ["/fastapi-sandbox/scripts/run_server.sh"]
