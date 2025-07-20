# Distributed Task Queue System

## Overview

This project implements a simple distributed task queue system with two services:

- **Task API Service**: Accepts and tracks tasks.
- **Worker Service**: Processes tasks asynchronously.

## Technologies

- FastAPI
- SQLite + SQLAlchemy
- httpx (for async service-to-service calls)

## Setup

### 1. Clone and Set Up Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create .env

```bash
cp .env.example .env
```

### 3. Run Both Services in Separate Terminals

#### Terminal 1: Task API Service

```bash
uvicorn task_api_service.main:app --port 8000 --reload
```

#### Terminal 2: Worker Service

```bash
uvicorn worker_service.main:app --port 8001 --reload
```

## API Usage

### Create Task

```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" \
     -d '{"task_type": "reverse_string", "payload": "hello"}'
```

### Check Task

```bash
curl http://localhost:8000/tasks/1
```

## Notes

- Tasks can be of type: `echo`, `reverse_string`, or `cpu_intensive`.
- Worker will simulate a CPU task using `asyncio.sleep(10)`.
