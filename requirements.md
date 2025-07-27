---

# 📄 Project Requirements: Async Document Q\&A Microservice with Mock LLM

## 🧠 Use Case Description

You're building a backend microservice for an **AI-powered Document Q\&A application**.

The service allows users to:

* Upload a document
* Ask questions about a specific document
* Receive an answer (generated asynchronously by a simulated/mock LLM)

This project is designed to demonstrate:

* Python backend engineering
* Async programming
* Database modeling
* Clean API design using FastAPI

---

## 🚀 Features to Implement

### 1. Document Upload & Storage

* Accept and store a document with:

  * `title`: str
  * `content`: str

### 2. Document Retrieval

* Retrieve a specific document by ID

### 3. Question Submission

* Ask a question related to a specific document
* Store the question and its relation to the document
* Simulate answer generation with a delay

### 4. Asynchronous Answer Generation

* Use `asyncio.create_task()` to simulate background LLM work
* Simulate latency with `await asyncio.sleep(5)`
* Return dummy answer:

  ```
  "This is a generated answer to your question: {question}"
  ```
* Support querying the question’s status: `pending` or `answered`

---

## 🌐 API Endpoints

| Endpoint                   | Method | Description                            |
| -------------------------- | ------ | -------------------------------------- |
| `/documents/`              | `POST` | Upload a document (`title`, `content`) |
| `/documents/{id}`          | `GET`  | Get document by ID                     |
| `/documents/{id}/question` | `POST` | Ask a question about a document        |
| `/questions/{id}`          | `GET`  | Get status and answer to a question    |
| `/health`                  | `GET`  | Health check route                     |

---

## 🧰 Technical Requirements

### ✅ Backend

* Use **FastAPI** for API server
* Use **async Python** throughout
* Organize the app modularly:

  ```
  app/
  ├── routes/
  ├── services/
  ├── schemas.py
  ├── models.py
  ├── database.py
  └── main.py
  ```

### ✅ Database (PostgreSQL)

Use async SQLAlchemy and PostgreSQL to store:

#### `documents`

| Field   | Type            |
| ------- | --------------- |
| id      | UUID / int (PK) |
| title   | str             |
| content | str             |

#### `questions`

| Field        | Type                          |
| ------------ | ----------------------------- |
| id           | UUID / int (PK)               |
| document\_id | FK to documents               |
| question     | str                           |
| answer       | str (nullable)                |
| status       | enum: `pending` \| `answered` |
| created\_at  | datetime                      |

---

## 🐳 Optional: Dockerization

Add support for running the app with Docker:

### Dockerfile

* Use `python:3.10` base
* Install dependencies and run `uvicorn`

### docker-compose.yml

* Include FastAPI app container
* Include PostgreSQL container
* Support `.env` config for DB

---

## ✅ Bonus Requirements (Optional but recommended)

* ✅ Use `Pydantic` for request/response validation
* ✅ Log incoming API requests and background events
* ✅ Add a `/health` endpoint to check app status
* ✅ Add `.env.example` for env configuration
* ✅ Add `README.md` with setup and usage instructions
* ✅ Write unit tests for services or route handlers
* ✅ Build a Postman collection or API usage doc

---

