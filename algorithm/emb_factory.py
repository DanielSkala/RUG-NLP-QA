from abc import ABC, abstractmethod
from algorithm.models import EmbeddingEntry


class EmbeddingFactory(ABC):

    @abstractmethod
    def store(self, embeddings: [EmbeddingEntry], *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def retrieve(self, embedding: [float], *args, **kwargs) -> [EmbeddingEntry]:
        pass
