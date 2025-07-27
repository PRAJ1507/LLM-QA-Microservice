from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Question, QuestionStatus
from app.schemas import QuestionCreate
from app.models import Document
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

async def create_question(db: AsyncSession, document_id: int, question_data: QuestionCreate) -> Question:
    question = Question(document_id=document_id, question=question_data.question)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question

async def get_question(db: AsyncSession, question_id: int) -> Question | None:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()

async def generate_answer_with_ollama(document_content: str, question: str) -> str:
    prompt = f"Answer the following question based on the document:\n\n{document_content}\n\nQ: {question}"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()

async def answer_question(db: AsyncSession, question: Question, document: Document) -> Question:
    answer = await generate_answer_with_ollama(document.content, question.question)
    question.answer = answer
    question.status = QuestionStatus.answered
    await db.commit()
    await db.refresh(question)
    return question
