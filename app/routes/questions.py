from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import AsyncSessionLocal
from app import models, schemas
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma

router = APIRouter(tags=["Questions"])

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Background RAG Task
async def rag_llm_answer(question_id: int, question_text: str, doc_id: int):
    # 1. Load vectorstore
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    # 2. Retrieve relevant content
    docs = vectorstore.similarity_search(
        query=question_text,  # Corrected parameter name
        k=4,
        filter={"doc_id": str(doc_id)}
    )
    context = "\n".join([d.page_content for d in docs]) or "No relevant content found."

    # 3. Generate answer
    llm = ChatOllama(model="llama3.2", temperature=0.2)
    prompt = f'''You are a highly skilled document analysis expert.

    Your task is to read and understand the content of the document provided below. Based on this document, you will answer the user's question **only using information present in the document**. Do not hallucinate or add assumptions beyond the provided content.

    If the answer cannot be found in the document, clearly state that the information is not available.

    ---

    Document:
    {context}

    ---

    Question:
    {question_text}

    ---

    Instructions:
    - Provide concise, accurate answers.
    - Quote or refer to the document where appropriate.
    - If the document does not contain the answer, respond with: “The document does not provide this information.'''

    result = llm.invoke(prompt)

    # 4. Save answer in DB using a new session
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(models.Question).where(models.Question.id == question_id))
        question = res.scalar_one_or_none()

        if question:
            question.answer = result.content.strip()
            question.status = models.QuestionStatus.answered
            await db.commit()

# Ask a question
@router.post("/documents/{doc_id}/question", response_model=schemas.QuestionResponse)
async def ask_question(
    doc_id: int,
    question_data: schemas.QuestionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Document).where(models.Document.id == doc_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    question = models.Question(
        document_id=doc_id,
        question=question_data.question,
        status=models.QuestionStatus.pending,
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)

    background_tasks.add_task(rag_llm_answer, question.id, question.question, doc_id)

    return question

# Get question by ID
@router.get("/questions/{id}", response_model=schemas.QuestionResponse)
async def get_question(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Question).where(models.Question.id == id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

# List all questions for a document
@router.get("/documents/{doc_id}/questions", response_model=list[schemas.QuestionResponse])
async def list_questions_for_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Question).where(models.Question.document_id == doc_id))
    return result.scalars().all()
