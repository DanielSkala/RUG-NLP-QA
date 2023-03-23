from fastapi import FastAPI
from algorithm.ir_system import IRSystem
from algorithm.document_operator import PDFDocumentOperator
from algorithm.embedding_operator import ModelEmbeddingOperator, OpenAIEmbeddingOperator
from algorithm.embedding_factory import ESEmbeddingFactory
from algorithm.document_factory import ESDocumentFactory
from algorithm.caching_strategy import PDFChunkingCachingStrategy
from algorithm.answer_strategy import OpenAIAnswerStrategy
from utils.path import get_absolute_path

es_client_params = {
    "hosts": "http://localhost:9200",
}

embedding_index_name = 'example_embedding_index_3_openai'
document_index_name = 'example_document_index_3_openai'

caching_strategy = PDFChunkingCachingStrategy(
    document_factory=ESDocumentFactory(es_client_params, index_name=document_index_name),
    embedding_factory=ESEmbeddingFactory(es_client_params, embedding_size=512,
                                         index_name=embedding_index_name),
    # embedding_operator=ModelEmbeddingOperator(
    #     get_absolute_path('../artifacts/distiluse-base-multilingual-cased-v1')),
    embedding_operator=OpenAIEmbeddingOperator("text-embedding-ada-002"),
    document_operator=PDFDocumentOperator()
)

ir_system = IRSystem(
    caching_strategy=caching_strategy,
    answer_strategy=OpenAIAnswerStrategy("text-davinci-003")
)

app = FastAPI()


@app.get("/doc/{document_id}/_index")
def find(document_id: str, q: str):
    return ir_system.find(document_id, q)
