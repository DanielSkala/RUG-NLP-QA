import os.path

from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator
from algorithm.embedding_operator import ModelEmbeddingOperator, OpenAIEmbeddingOperator
from algorithm.models import Document
from algorithm.embedding_factory import ESEmbeddingFactory
from algorithm.document_factory import ESDocumentFactory
from algorithm.caching_strategy import PDFChunkingCachingStrategy
from algorithm.answer_strategy import SentenceTransformerAnswerStrategy
from utils.path import get_absolute_path

es_client_params = {
    "hosts": "http://localhost:9200",
}

embedding_index_name = 'example_embedding_index_3_openai'
document_index_name = 'example_document_index_3_openai'

pdf_path = input("Enter the path of the pdf file: ")
id_name = input("Enter the id of the pdf file: ")

if __name__ == '__main__':
    doc = Document(
        id=id_name,
        data=pdf_path
    )

    # FIXME: THE EMBEDDING SIZE NEEDS TO BE ADJUSTED TO THE CORRECT VALUE
    embedding_factory = ESEmbeddingFactory(es_client_params, embedding_size=1536,
                                           index_name=embedding_index_name)
    document_factory = ESDocumentFactory(es_client_params, index_name=document_index_name)

    # Reset the index
    embedding_factory.clear()
    document_factory.clear()

    caching_strategy = PDFChunkingCachingStrategy(
        document_factory=document_factory,
        embedding_factory=embedding_factory,
        embedding_operator=ModelEmbeddingOperator(
            get_absolute_path('../artifacts/multi-qa-MiniLM-L6-cos-v1')),
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
