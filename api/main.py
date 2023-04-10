from fastapi import FastAPI
from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator

from algorithm.caching_strategy import PDFChunkingCachingStrategy
import settings

caching_strategy = PDFChunkingCachingStrategy(
    document_factory=settings.document_factory,
    embedding_factory=settings.embedding_factory,
    embedding_operator=settings.embedding_operator,
    # embedding_operator=OpenAIEmbeddingOperator("text-embedding-ada-002"),
    document_operator=PDFDocumentOperator()
)

ir_system = IRSystem(
    answer_strategy=settings.answer_strategy,
    caching_strategy=caching_strategy,
)

app = FastAPI()


@app.get("/doc/{document_id}/_index")
def find(document_id: str, q: str):
    return ir_system.find(document_id, q)
