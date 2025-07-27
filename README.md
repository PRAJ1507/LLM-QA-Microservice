# LLM QA Microservice

This project is a microservice for managing documents and answering questions using LLMs (Large Language Models). Follow the steps below to set up and run the project.

## Prerequisites

- Ensure you have Python installed on your system.
- Install the `uv` package manager. You can find the installation guide [here](https://uv.pm/docs).
- Must have postgre db running.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm_qa_microservice
   ```
2. Install the required dependencies:
   ```bash
   uv add -r requirements.txt
   ```
## Creating tables

To create tables run the following command:

```bash
uv run postgredb_runfirst.py
```

## Running the Microservice

To run the microservice, use the following command:

```bash
uv run uvicorn app.main:app --reload
```

## Usage

Once the microservice is running, you can access it at `http://localhost:8000`. You can use tools like Postman or CURL to interact with the API endpoints.

## Running the Streamlit App

To start the Streamlit app, use the following command:

```bash
streamlit run app.py
```

