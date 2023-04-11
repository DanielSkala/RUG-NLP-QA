
from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator
from algorithm.models import Document
from algorithm.caching_strategy import PDFChunkingCachingStrategy
from algorithm.answer_strategy import SentenceTransformerAnswerStrategy
import settings

pdf_path = None
id_name = "test"

MODEL_NAME = "distiluse-base-multilingual-cased-v1"
MODEL_EMBEDDING_SIZE = 512

if __name__ == '__main__':
    doc = Document(
        id=id_name,
        data=pdf_path
    )

    # Reset the index
    settings.embedding_factory.clear()
    settings.document_factory.clear()

    caching_strategy = PDFChunkingCachingStrategy(
        document_factory=settings.document_factory,
        embedding_factory=settings.embedding_factory,
        embedding_operator=settings.embedding_operator,
        # embedding_operator=OpenAIEmbeddingOperator("text-embedding-ada-002"),
        document_operator=PDFDocumentOperator(),
        chunk_size=5,
        sentence_word_count=(10, 20)
    )

    ir_system = IRSystem(
        caching_strategy=caching_strategy,
        answer_strategy=SentenceTransformerAnswerStrategy("../artifacts/gpt2")
    )

    ir_system.index_document(doc)
