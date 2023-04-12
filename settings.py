from utils.path import get_absolute_path
from algorithm.embedding_operator import ModelEmbeddingOperator, OpenAIEmbeddingOperator
from algorithm.embedding_factory import ESEmbeddingFactory
from algorithm.document_factory import ESDocumentFactory
from algorithm.answer_strategy import OpenAIAnswerStrategy, SentenceTransformerAnswerStrategy


EMBEDDING_INDEX_NAME = 'embedding_index'
DOCUMENT_INDEX_NAME = 'document_index'

es_client_params = {
    "hosts": "http://localhost:9200",
}

# ATTENTION: if u change the model name, u need to change the embedding size

embedding_operator = ModelEmbeddingOperator(get_absolute_path('../artifacts/distiluse-base-multilingual-cased-v1'))
document_factory = ESDocumentFactory(es_client_params, index_name=DOCUMENT_INDEX_NAME)
embedding_factory = ESEmbeddingFactory(es_client_params, embedding_size=512, index_name=EMBEDDING_INDEX_NAME)

# answer_strategy = OpenAIAnswerStrategy("text-davinci-003")
answer_strategy = SentenceTransformerAnswerStrategy(get_absolute_path('../artifacts/gpt2'))
