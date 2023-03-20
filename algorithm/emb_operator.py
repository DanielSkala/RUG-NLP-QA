from abc import ABC, abstractmethod
from algorithm.models import TextEntry, EmbeddingEntry
from sentence_transformers import SentenceTransformer


class EmbeddingOperator(ABC):
    @abstractmethod
    def embed(self, entries: [TextEntry], *args, **kwargs) -> [EmbeddingEntry]:
        pass


class ModelEmbeddingOperator(EmbeddingOperator):

    def __init__(self, model_name: str):
        self.model_name = model_name

    def embed(self, entries: [TextEntry], *args, **kwargs) -> [EmbeddingEntry]:
        model = SentenceTransformer(self.model_name)
        embeddings = model.encode([entry.text for entry in entries])
        return [
            EmbeddingEntry(
                id=entry.id,
                embedding=list(embedding),
                metadata=entry.metadata
            ) for entry, embedding in
            zip(entries, embeddings)]


if __name__ == '__main__':
    operator = ModelEmbeddingOperator('distiluse-base-multilingual-cased-v1')
    entries = [
        TextEntry(
            id="1",
            text='hello world',
            metadata={}
        ),
        TextEntry(
            id="2",
            text='gay',
            metadata={}
        ),
    ]

    embeddings = operator.embed(entries)
    print(embeddings)
