📘 API Documentation (LLM Q&A over Documents)
🔗 Base URL:
```bash
http://localhost:8000
```

📄 1. Upload Document
POST /documents/
Upload and embed a document.

Request Body (JSON):
```bash
{
  "title": "Sample Document",
  "content": "This is the full content of the document."
}
```
Response (200 OK):
```bash
{
  "id": 1,
  "title": "Sample Document",
  "content": "This is the full content of the document."
}
```


📚 2. List All Documents
GET /documents/

Response:
```bash
[
  {
    "id": 1,
    "title": "Sample Document",
    "content": "This is the full content of the document."
  },
  ...
]
```


❌ 3. Delete Document
DELETE /documents/{id}
Also deletes related Chroma chunks.

Response:
```bash
{"detail": "Document deleted successfully"}
```


❓ 4. Ask a Question
POST /documents/{doc_id}/question
Asynchronously submits a question for a document.

Path Parameter:
doc_id: ID of the document

Request Body (JSON):
```bash
{
  "question": "What is this document about?"
}
```
Response:
```bash
{
  "id": 5,
  "question": "What is this document about?",
  "status": "pending",
  "answer": null,
  "document_id": 1
}
```
⌛ 5. Get Question + Answer
GET /questions/{id}

Response:
```bash
{
  "id": 5,
  "question": "What is this document about?",
  "status": "answered",
  "answer": "The document discusses...",
  "document_id": 1
}
```


📝 6. List All Questions for a Document
GET /documents/{doc_id}/questions

Response:
```bash
[
  {
    "id": 1,
    "question": "First question",
    "status": "answered",
    "answer": "Answer content",
    "document_id": 1
  },
  ...
]
```


📦 Postman Collection (JSON)
You can copy and import the below into Postman via File → Import → Raw Text.

 Postman Collection JSON
```bash
{
  "info": {
    "name": "LLM QA API",
    "_postman_id": "llm-qa-collection",
    "description": "Interact with document upload and LLM Q&A",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Upload Document",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"title\": \"Sample Doc\",\n  \"content\": \"This is sample document content.\"\n}"
        },
        "url": { "raw": "http://localhost:8000/documents/", "host": ["localhost"], "port": "8000", "path": ["documents"] }
      }
    },
    {
      "name": "List Documents",
      "request": {
        "method": "GET",
        "url": { "raw": "http://localhost:8000/documents/", "host": ["localhost"], "port": "8000", "path": ["documents"] }
      }
    },
    {
      "name": "Delete Document",
      "request": {
        "method": "DELETE",
        "url": { "raw": "http://localhost:8000/documents/1", "host": ["localhost"], "port": "8000", "path": ["documents", "1"] }
      }
    },
    {
      "name": "Ask Question",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"question\": \"What is the document about?\"\n}"
        },
        "url": { "raw": "http://localhost:8000/documents/1/question", "host": ["localhost"], "port": "8000", "path": ["documents", "1", "question"] }
      }
    },
    {
      "name": "Get Question by ID",
      "request": {
        "method": "GET",
        "url": { "raw": "http://localhost:8000/questions/1", "host": ["localhost"], "port": "8000", "path": ["questions", "1"] }
      }
    },
    {
      "name": "List Questions for a Document",
      "request": {
        "method": "GET",
        "url": { "raw": "http://localhost:8000/documents/1/questions", "host": ["localhost"], "port": "8000", "path": ["documents", "1", "questions"] }
      }
    }
  ]
}
```
