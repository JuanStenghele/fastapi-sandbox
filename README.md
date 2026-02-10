# FastAPI Sandbox

Example web API for testing and learning new stuff. Developed in Python 3.10 using FastAPI.

## Requirements

- docker (v24.0.2 OK)

## How to run

### Docker compose

This repository contains a `docker-compose.yml` to run the API, the Postgres DB and DB migrations (automatically run). To do so, rename the `.env.example` file to `.env` and run:

```bash
docker compose build
docker compose up
```

The API will be running on `http://localhost:8000/`.

### Kubernetes

Run minikube:

```bash
minikube start --driver=docker
```

Build API Docker image:

```bash
docker build . -t fastapi-sandbox
```

Upload to Minikube the docker image:

```bash
minikube image load fastapi-sandbox
```

Add the required secrets by moving the `.template.yml` into `.yml` files and replace the `${ENV_VARS}` with the custom credentials.

Apply the local setup:

```bash
kubectl apply --recursive -f kubernetes
```

Open dashboard:

```bash
minikube dashboard
```

Access the FastAPI Swagger by running:

```bash
minikube tunnel
```

And accessing `http://localhost/docs`

Forward API to local:

```bash
minikube service fastapi-sandbox-service
```

Restart deployments:

```bash
kubectl rollout restart deployments
```

## Tests

To run the tests execute:

```bash
python -m pytest
```

## EKS

The Dev Container contains all the dependencies installed to run this section. Configure AWS credentials:

```bash
aws configure
```

Add EKS context:

```bash
aws eks --region us-east-1 update-kubeconfig --name juans-fastapi-sandbox-eks
```

Now `kubectl` can be used:

```bash
kubectl cluster-info
```
