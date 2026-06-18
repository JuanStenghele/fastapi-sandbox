# FastAPI Sandbox

Example web API for testing and learning new stuff. Developed in Python 3.13 using FastAPI.

## Requirements

- docker (v24.0.2 OK)

## How to run

### Docker compose

This repository contains a `docker-compose.yml` to run the API, the Postgres DB and DB migrations (automatically run). To do so, rename the `.env.example` file to `.env` and run:

```bash
docker compose build
docker compose up -d
```

The API will be running on `http://localhost:8000/`.

### Helm/Kubernetes

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

Make sure `kubectl` points to `minikube`:

```bash
kubectl config use-context minikube
```

Install Helm dependencies in the `helm` directory with:

```bash
cd helm
helm dependency build
```

Apply the rest of the stack with Helm:

```bash
helm upgrade --install fastapi-sandbox helm/ -f helm/values.yaml -f helm/values.local.yaml
```

Forward services by running:

```bash
kubectl port-forward svc/fastapi-sandbox-traefik 8000:80
```

And accessing:

- http://api.127.0.0.1.nip.io:8000/docs
- http://grafana.127.0.0.1.nip.io:8000
- http://headlamp.127.0.0.1.nip.io:8000
- http://minio.127.0.0.1.nip.io:8000

Open dashboard:

```bash
minikube dashboard
```

Restart deployments:

```bash
kubectl rollout restart deployments
```

Helm lint:

```bash
helm lint helm/ -f helm/values.yaml -f helm/values.local.yaml
```

Generate headlamp token with:

```bash
kubectl create token headlamp
```

### Auth

The API uses OAuth 2.0 with JWT bearer tokens. In production, Auth0 should act as the identity provider. Locally, [mock-oauth2-server](https://github.com/navikt/mock-oauth2-server) replaces it: it implements the same protocol, issues real JWTs and exposes a JWKS endpoint, so the application code is identical in both environments. This avoids hitting a real Auth0 tenant during development and system tests and avoids adding an external dependency to the local stack. However, Auth0 can be also used locally for testing purposes if needed.

#### mock-oauth2-server

`.env.example` credentials are prepared to use this service, so no changes are needed.

Generate a local access token:

```bash
curl -X POST http://localhost:8080/fastapi-sandbox/token -d "grant_type=client_credentials&client_id=<your-id>&client_secret=test&scope=admin"
```

Remember to replace `<your-id>` with the ID of the user you want to authenticate as. This value will be returned in the `sub` claim.

Or it can be done from the [UI](http://localhost:8080/fastapi-sandbox/debugger) clicking on `GET A TOKEN` and then entering any user. Make sure the application stack is running.

#### Auth0

Update the credential in the `.env` file to use Auth0.

- `AUTH_ISSUER=https://<your-tenant>.us.auth0.com/`: Get your tenant on the top left of the Auth0 dashboard or in `Applications > [Your App] > Settings > Domain`.
- `AUTH_AUDIENCE=https://<your-api-identifier>`: Found in `APIs > [Your API] > Settings > Identifier` (starts with `https://`).
- `AUTH_JWKS_URI=https://<your-tenant>.us.auth0.com/.well-known/jwks.json`: Same tenant as `AUTH_ISSUER`.

Generate a machine-to-machine token (`sub` claim will be your application's client ID, not a user ID) using the API Test tab: `APIs > [Your API] > Test`. Use the `curl` command displayed.

### Terraform

Build the AWS infraestructure using Terraform. First, create the `.tfvars` file:

```bash
cp terraform/infrastructure/terraform.tfvars.example terraform/infrastructure/terraform.tfvars
```

Then populate it with your own AWS credentials and choose a username and password for RDS service DB. Continue by initializing Terraform with: 

```bash
cd terraform/infrastructure
terraform init
```

Review the planned changes with:

```bash
terraform plan
```

Build the infraestructure with:

```bash
terraform apply
```

Delete everything with:

```bash
terraform destroy
```

To deploy the post-deployment configuration (DNS, K8s dashboard, ...) and use a custom domain. Run exactly the same but with the `post-deployment` directory:

```bash
cp terraform/post-deployment/terraform.tfvars.example terraform/post-deployment/terraform.tfvars
# Populate terraform/post-deployment/terraform.tfvars here
cd terraform/post-deployment
terraform init
terraform plan
terraform apply
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
