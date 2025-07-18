

# 🚀 Simple FastAPI EDA with Auth & Persistence

A production-grade, beginner-friendly **Event-Driven Architecture (EDA)** starter project using **FastAPI**, **Celery**, **Redis**, and **Docker**, now enhanced with **JWT authentication**, **task retries**, **task history**, and **persistent result storage** in **SQLite3**. Perfect for showcasing real-world async systems in interviews or demos.

---

## ⚙️ Core Features

* ✅ **Asynchronous Task Processing**
  Submit long-running tasks via `/submit` endpoint using Celery.

* 🔐 **JWT Authentication for Protected Routes**
  Secure all API endpoints (`/submit`, `/status/{task_id}`, `/history`) with token-based access.

* 📍 **Task Status Tracking**
  Retrieve task result and execution state using `/status/{task_id}`.

* 🧾 **Task History Endpoint**
  View a list of all completed task results from the SQLite DB via `/history`.

* ♻️ **Automatic Retry Mechanism**
  Automatically retries failed tasks (with delay and max retries).

* 💾 **Persistent Result Storage**
  All tasks and results are saved in SQLite3 for historical lookup.

* 🌸 **Real-Time Monitoring with Flower**
  Visualize task queues in your browser at `localhost:5555`.

---

## 🧰 Tech Stack Overview

| Component  | Role                                           |
| ---------- | ---------------------------------------------- |
| 🚀 FastAPI | API server and route handling                  |
| ⚙️ Celery  | Task queue & background execution engine       |
| 🧠 Redis   | Message broker for Celery tasks                |
| 🐳 Docker  | Containerization for reproducible environments |
| 🐍 SQLite3 | Persistent task metadata + result storage      |
| 🌸 Flower  | Celery web-based monitoring dashboard          |
| 🔑 PyJWT   | JWT-based authentication for API access        |

---

## 🔐 Authentication

All endpoints require a valid JWT token in the `Authorization` header:

```http
Authorization: Bearer <your_token>
```

### Sample Token for Testing

```bash
curl -X POST http://localhost:8000/token \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
```

---

## 🚀 Getting Started

### 1️⃣ Build and start all services

```bash
docker compose up --build
```

### 2️⃣ Get JWT Token

```bash
curl -X POST http://localhost:8000/token \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass"}'
```

### 3️⃣ Submit a Task

```bash
curl -X POST http://localhost:8000/submit \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"data": "your task input"}'
```

### 4️⃣ Check Task Status

```bash
curl -X GET http://localhost:8000/status/<task_id> \
     -H "Authorization: Bearer <token>"
```

### 5️⃣ View Task History

```bash
curl -X GET http://localhost:8000/history \
     -H "Authorization: Bearer <token>"
```

---

## 🧪 Task Retry Behavior

Each Celery task is automatically retried if it fails due to transient issues.

* 🔁 **Max Retries**: 3
* ⏱️ **Retry Delay**: 10 seconds

---

## 🌸 Monitor with Flower

Access Flower UI for task queue monitoring:

```
http://localhost:5555
```

---

## 🧑‍💼 Ideal For:

* 💼 Developers preparing for **interviews or demos**
* 🎓 Students and juniors learning **EDA and background tasks**
* 🏗️ Engineers designing **scalable async systems**
* 📦 Candidates showcasing **production-grade Dockerized APIs**

---

