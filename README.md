# CloudPulse

CloudPulse is an enterprise-style DevOps project demonstrating an end-to-end CI/CD pipeline.

![CI](https://github.com/Tanmay-hue/CloudPulse/actions/workflows/ci.yml/badge.svg)

## Tech Stack

- FastAPI
- Docker
- GitHub Actions
- Docker Hub
- Kubernetes
- Prometheus
- Grafana

## Features

- REST API
- Dockerized Application
- Automated CI/CD
- Kubernetes Deployment
- Monitoring
- Metrics
- Rolling Updates

## Architecture

Developer

↓

GitHub

↓

GitHub Actions

↓

Docker Hub

↓

Kubernetes

↓

Prometheus

↓

Grafana

## Docker

Build

```bash
docker build -t cloudpulse .
```

Run

```bash
docker run -p 8000:8000 cloudpulse
```

Docker Compose

```bash
docker compose up -d
```

## Monitoring

CloudPulse exposes Prometheus metrics at:

```
/metrics
```

Monitoring Stack

- Prometheus
- Grafana

Features

- Request Counter
- Health Endpoint
- Metrics Endpoint
- Dashboard Ready