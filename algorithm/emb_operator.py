from abc import ABC, abstractmethod
from algorithm.models import TextEntry, EmbeddingEntry


class EmbeddingOperator(ABC):
    @abstractmethod
    def embed(self, entries: [TextEntry], *args, **kwargs) -> [EmbeddingEntry]:
        pass
