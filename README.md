
# 🚀 Simple FastAPI EDA

A production-ready, beginner-friendly **Event-Driven Architecture (EDA)** starter project built with **FastAPI**, **Celery**, **Redis**, and **Docker**. Designed for showcasing background task processing with real-world features like task history, retry mechanisms, and result persistence.

---

## ⚙️ Core Functionality

- ✅ **Asynchronous Task Processing** – Submit long-running tasks via `/submit` endpoint.
- 📍 **Task Status Tracking** – Get task status and result using `/status/{task_id}`.
- 🧾 **Task History Endpoint** – View all completed task results from SQLite using `/history`.
- ♻️ **Automatic Retry Mechanism** – Tasks will automatically retry if failures occur.
- 💾 **Persistent Result Storage** – Results are saved in a SQLite database.
- 🌸 **Monitoring with Flower** – Real-time task queue monitoring via a UI (`localhost:5555`).

---

## 🧰 Tech Stack

| Component  | Purpose                              |
|------------|--------------------------------------|
| 🚀 FastAPI  | Web framework for REST APIs          |
| ⚙️ Celery   | Distributed task queue               |
| 🧠 Redis    | Message broker for task queuing      |
| 🐳 Docker   | Containerization                     |
| 🐍 SQLite3 | Store task metadata and results       |
| 🌸 Flower   | Celery monitoring dashboard          |

---

# Build and start all services
docker compose up --build


---

## 🌐 API Endpoints

| Method | Endpoint            | Description                     |
| ------ | ------------------- | ------------------------------- |
| POST   | `/submit`           | Submit a new background task    |
| GET    | `/status/{task_id}` | Check the status of a task      |
| GET    | `/history`          | View all completed task results |

---

## 📈 Monitoring

You can monitor task queues using **Flower UI**:

```bash
http://localhost:5555
```

---

## 👨‍💼 Who Is This For?

This project is perfect for:

* ✅ Developers learning **EDA and background processing**
* 🚀 Candidates building **technical portfolios**
* 💼 Engineers preparing for **interviews and demos**
* 🧪 Those experimenting with **Celery + FastAPI architecture**

---


