# Music Streaming Backend (AWS Cloud Architecture)

This repository contains the backend implementation of a cloud-based music streaming service. The backend is developed using **FastAPI** and is deployed on AWS using two architectures:

- **EC2-Only Architecture** (monolithic)
- **Hybrid Architecture** (EC2 + AWS Lambda + API Gateway)

---

## 🏗️ Architecture Branches

| Branch Name          | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `backend-dev`        | Backend designed for EC2-only deployment (monolithic setup) |
| `hybrid-backend-dev` | Modular backend for hybrid deployment with Lambda           |

---

## 🔧 Technologies Used

- **FastAPI** (Python backend)
- **Gunicorn + Uvicorn workers**
- **PostgreSQL (via AWS RDS)**
- **AWS EC2, ALB, Auto Scaling**
- **AWS Lambda & API Gateway**
- **AWS Secrets Manager**
- **Amazon CloudWatch** (dashboards & alarms)
- **AWS CloudFormation** (Infrastructure as Code)

---

## 🚀 Deployment Overview

### EC2-Only Architecture

- Uses `backend-dev` branch.
- Backend is deployed to EC2 using a Launch Template and Auto Scaling Group.
- Exposed via an Application Load Balancer (ALB).
- CloudWatch monitors performance using EC2-specific metrics and alarms.

### Hybrid Architecture

- Uses the `hybrid-backend-dev` branch.
- Backend logic is modularized to support deployment across both **EC2 and Lambda**.
- Folder structure:
  - `EC2app/` contains the FastAPI application for EC2 deployment.
  - `auth_lambda/` and `songs_lambda/` contain Lambda function handlers for the `/auth` and `/songs` routes.
- Lambda functions are connected via API Gateway and provisioned with concurrency (for auth).
- EC2 still handles heavier operations like media streaming.

---

To deploy the Lambda functions via CloudFormation and S3, run the provided shell scripts to automatically package each Lambda directory:

```bash
# Build /auth Lambda ZIP
./build_auth_lambda.sh

# Build /songs Lambda ZIP
./build_songs_lambda.sh
```
