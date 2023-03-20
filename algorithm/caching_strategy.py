from abc import ABC, abstractmethod
from algorithm.models import TextEntry, EmbeddingEntry
from algorithm.embedding_operator import EmbeddingOperator
from algorithm.embedding_factory import EmbeddingFactory
from algorithm.document_factory import DocumentFactory
from algorithm.document_operator import DocumentOperator


class CachingStrategy(ABC):

    def __init__(self,
                 embedding_factory: EmbeddingFactory,
                 document_factory: DocumentFactory,
                 embedding_operator: EmbeddingOperator,
                 document_operator: DocumentOperator):
        self.embedding_factory = embedding_factory
        self.document_factory = document_factory
        self.embedding_operator = embedding_operator
        self.document_operator = document_operator

    @abstractmethod
    def cache(self, document, *args, **kwargs) -> [TextEntry]:
        pass

    def _find_relevant_embedding_entries(self, query: str, *args, **kwargs) -> [EmbeddingEntry]:
        embedding = self.embedding_operator.embed(query)
        return self.embedding_factory.retrieve(embedding)

    def find(self, query: str, *args, **kwargs) -> [TextEntry]:
        relevant_entries = self._find_relevant_embedding_entries(query, *args, **kwargs)
        return self.document_operator.retrieve([entry.id for entry in relevant_entries], *args,
                                               **kwargs)
