# 🚀 IoT Telemetry Microservices — Kubernetes POC

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-POC-success)

A hands-on **IoT telemetry ingestion platform POC** demonstrating how a containerized Python service can be deployed on Kubernetes and securely connect to PostgreSQL for backend validation.

The project is intentionally small, but it reflects several patterns used in real platform engineering environments: **containerization, Kubernetes workload/service separation, configuration through environment variables, secret-backed database credentials, health endpoints, and database connectivity testing**.

## 🎯 What This POC Demonstrates

- Build and package a Python Flask service into a Docker image
- Deploy the application as a Kubernetes `Deployment`
- Expose the application through a Kubernetes `Service`
- Run PostgreSQL inside Kubernetes
- Store database credentials using a Kubernetes `Secret`
- Connect the application to PostgreSQL using environment-based configuration
- Validate application and database health through HTTP endpoints
- Manage the supporting PostgreSQL administration layer with pgAdmin

## 🏗️ Architecture

```text
                    ┌──────────────────────────────┐
                    │        IoT / Client           │
                    └──────────────┬───────────────┘
                                   │ HTTP
                                   ▼
                    ┌──────────────────────────────┐
                    │     Ingestion Service        │
                    │   Flask + Python + Docker    │
                    │         Port: 8080           │
                    └──────────────┬───────────────┘
                                   │
                         Kubernetes Service DNS
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       PostgreSQL             │
                    │        Port: 5432            │
                    └──────────────────────────────┘
                                   ▲
                                   │
                    ┌──────────────┴───────────────┐
                    │   Kubernetes Secret          │
                    │ DB User / Password / DB      │
                    └──────────────────────────────┘

                    ┌──────────────────────────────┐
                    │           pgAdmin            │
                    │  PostgreSQL administration   │
                    └──────────────────────────────┘
```

## 🧩 Project Structure

```text
iottelemetrymicroservices/
├── app/
│   ├── app.py                  # Flask ingestion API
│   ├── Dockerfile              # Container image definition
│   └── requirements.txt        # Python dependencies
│
├── ingestion-deployment.yaml   # Kubernetes Deployment
├── ingestion-service.yaml      # Kubernetes Service
├── postgres-pod.yaml           # PostgreSQL workload
├── postgres-service.yaml        # PostgreSQL Service
├── postgres-secret.yaml         # Database credentials
├── pgadmin.yaml                 # pgAdmin workload/service
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | Returns application name and running status |
| `GET /health` | Lightweight application health check |
| `GET /db-test` | Validates PostgreSQL connectivity and returns database/version information |

Example response from `/`:

```json
{
  "application": "Axion Ingestion Service",
  "status": "running"
}
```

The `/db-test` endpoint performs a PostgreSQL query using `current_database()` and `version()` and reports a `500` response when the database connection fails.

## ⚙️ Configuration

The application reads PostgreSQL connection settings from environment variables:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

In Kubernetes, the deployment injects database credentials from the `postgres-secret` Secret while using the Kubernetes service name `postgres-service` for service discovery.

> **Security note:** Do not commit real production credentials into Kubernetes manifests. For production deployments, prefer a managed secret solution such as a cloud secret manager, external-secrets pattern, or sealed/encrypted secrets.

## 🐳 Build the Container

From the repository root:

```bash
docker build -t axion-ingestion:v1 ./app
```

Run locally:

```bash
docker run --rm -p 8080:8080 \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=appdb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=<password> \
  axion-ingestion:v1
```

The application listens on port `8080`.

## ☸️ Kubernetes Deployment

Create the namespace used by the manifests:

```bash
kubectl create namespace axion
```

Apply PostgreSQL resources:

```bash
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-pod.yaml
kubectl apply -f postgres-service.yaml
```

Deploy pgAdmin:

```bash
kubectl apply -f pgadmin.yaml
```

Deploy the ingestion service:

```bash
kubectl apply -f ingestion-deployment.yaml
kubectl apply -f ingestion-service.yaml
```

Verify workloads:

```bash
kubectl get pods -n axion
kubectl get svc -n axion
kubectl get deployments -n axion
```

## 🔍 Validate the Application

Check pod status:

```bash
kubectl get pods -n axion -o wide
```

Inspect application logs:

```bash
kubectl logs -n axion deployment/ingestion-service
```

Port-forward the application locally:

```bash
kubectl port-forward -n axion service/ingestion-service 8080:8080
```

Then test:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/db-test
```

## 🧪 Troubleshooting Flow

A simple operational workflow for this POC is:

```text
Pod Running?
     │
     ├── No → kubectl describe pod / kubectl logs
     │
     ▼
Service Reachable?
     │
     ├── No → kubectl get svc / endpoints / port-forward
     │
     ▼
/health = healthy?
     │
     ├── No → inspect application logs
     │
     ▼
/db-test succeeds?
     │
     ├── No → verify Secret + PostgreSQL service + DB availability
     │
     ▼
✅ Application → Kubernetes → PostgreSQL validated
```

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Application | Python, Flask |
| API | HTTP/JSON |
| Database | PostgreSQL |
| Database Admin | pgAdmin |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Configuration | Environment Variables |
| Secrets | Kubernetes Secret |

## 💡 Platform Engineering Takeaways

This POC is useful as a foundation for expanding into a more production-oriented platform with:

- Kubernetes health/readiness probes
- Horizontal Pod Autoscaling
- Persistent volumes for PostgreSQL
- Ingress / API gateway integration
- Centralized logging and metrics
- Prometheus + Grafana observability
- Image vulnerability scanning with Trivy
- CI/CD with GitHub Actions or Azure DevOps
- Infrastructure as Code with Terraform
- Managed PostgreSQL instead of in-cluster database workloads
- External secret management and workload identity
- GitOps deployment using Argo CD or Flux

## 📌 POC Scope

This repository focuses on **Kubernetes deployment and service-to-database connectivity validation**. It is not intended to represent a complete production IoT ingestion platform yet.

The next evolution would be to add telemetry ingestion/persistence logic, asynchronous messaging (for example Kafka or Azure Event Hubs), persistent storage, observability, autoscaling, security controls, and automated CI/CD.

## 👨‍💻 Author

**Burhan Yousuf Wani**  
DevSecOps / Cloud Engineering | Kubernetes | Docker | Azure | Terraform

## ⭐ Why This Project Matters

This POC demonstrates the complete path from **application code → Docker container → Kubernetes workload → service discovery → PostgreSQL connectivity**, making it a practical foundation for modern cloud-native and DevSecOps workflows.

---

⭐ If you find the project useful, consider starring the repository and exploring the Kubernetes manifests to understand how each layer is wired together.
