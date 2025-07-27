from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Document
from app.schemas import DocumentCreate

async def create_document(db: AsyncSession, document: DocumentCreate) -> Document:
    db_doc = Document(title=document.title, content=document.content)
    db.add(db_doc)
    await db.commit()
    await db.refresh(db_doc)
    return db_doc

async def get_document(db: AsyncSession, document_id: int) -> Document | None:
    result = await db.execute(select(Document).where(Document.id == document_id))
    return result.scalar_one_or_none()
