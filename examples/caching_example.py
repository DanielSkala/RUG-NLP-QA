from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator
from algorithm.embedding_operator import ModelEmbeddingOperator
from algorithm.models import Document
from algorithm.embedding_factory import ESEmbeddingFactory
from algorithm.document_factory import ESDocumentFactory
from algorithm.caching_strategy import PDFChunkingCachingStrategy
from algorithm.answer_strategy import SentenceTransformerAnswerStrategy
from utils.path import get_absolute_path

es_client_params = {
    "hosts": "http://localhost:9200",
}

embedding_index_name = 'example_embedding_index'
document_index_name = 'example_document_index'

if __name__ == '__main__':
    doc = Document(
        id='project_plan.pdf',
        data='./Project plan.pdf'
    )

    caching_strategy = PDFChunkingCachingStrategy(
        document_factory=ESDocumentFactory(es_client_params, index_name=document_index_name),
        embedding_factory=ESEmbeddingFactory(es_client_params, embedding_size=512, index_name=embedding_index_name),
        embedding_operator=ModelEmbeddingOperator(
            get_absolute_path('../artifacts/distiluse-base-multilingual-cased-v1')),
        document_operator=PDFDocumentOperator()
    )

