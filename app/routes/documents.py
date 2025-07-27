from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app import models, schemas
from sqlalchemy.future import select
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument
from sqlalchemy import delete  # Import the delete function
import uuid

router = APIRouter(prefix="/documents", tags=["Documents"])


# Dependency to get async DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/", response_model=schemas.DocumentResponse)
async def create_document(
    doc: schemas.DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_doc = models.Document(title=doc.title, content=doc.content)

    try:
        # 1. Save to PostgreSQL
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)

        # 2. Split content
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = splitter.split_text(doc.content)

        # 3. Prepare Chroma documents
        langchain_docs = [
            LCDocument(
                page_content=chunk,
                metadata={"doc_id": str(new_doc.id), "chunk_id": str(uuid.uuid4())}
            )
            for chunk in chunks
        ]

        # 4. Embed and store in Chroma
        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        vectorstore.add_documents(langchain_docs)

        return new_doc

    except Exception as e:
        # 🧹 Rollback: delete from DB if Chroma step fails
        doc_id = new_doc.id  # Store the ID before rollback
        await db.rollback()
        await db.execute(
            delete(models.Document).where(models.Document.id == doc_id)
        )
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")


@router.get("/{id}", response_model=schemas.DocumentResponse)
async def get_document(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Document).where(models.Document.id == id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

@router.get("/", response_model=list[schemas.DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Document))
    documents = result.scalars().all()
    return documents

@router.delete("/{id}", response_model=dict)
async def delete_document(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Document).where(models.Document.id == id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete from DB
    await db.delete(document)
    await db.commit()

    # Delete Chroma chunks
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    vectorstore.delete(filter={"doc_id": str(id)})

    return {"detail": "Document and related chunks deleted"}

@router.get("/{id}/questions", response_model=list[schemas.QuestionResponse])
async def list_questions_for_document(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Question).where(models.Question.document_id == id))
    return result.scalars().all()
