from abc import ABC, abstractmethod
from algorithm.models import TextEntry, EmbeddingEntry
from algorithm.embedding_operator import EmbeddingOperator
from algorithm.embedding_factory import EmbeddingFactory
from algorithm.document_factory import DocumentFactory, generate_id
from algorithm.document_operator import DocumentOperator
from typing import List

"""
CachingStrategy is an abstract class that defines the interface for caching strategies.

Responsibilities: 
    - Manipulates the document and converts into a list of TextEntry and EmbeddingEntry objects.
    - Utilises the factories to store the entries.
    - Utilises the operators to parse the documents and embed the text.
    - finding relevant documents given a query in accordance with the way the entries returning the list of ids.
    
"""


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

    """
    Caches the document in embedding and text entry forms.
    :parameter document: The document to be cached of any type.
    """

    @abstractmethod
    def cache(self, document, *args, **kwargs):
        pass

    def _get_matching_embeddings(self, doc_id, query: str, metadata: dict = None, *args, **kwargs) -> List[
        EmbeddingEntry]:
        embedding = self.embedding_operator.embed(query)
        matched_embeddings = self.embedding_factory.retrieve(doc_id, embedding, metadata=metadata)
        return matched_embeddings

    def _get_matching_text(self, doc_id, query: str, metadata: dict = None, *args, **kwargs) -> List[TextEntry]:
        matched_embeddings = self._get_matching_embeddings(doc_id, query, metadata=metadata)
        ids = [embedding.id for embedding in matched_embeddings]
        matched_text = self.document_factory.retrieve(doc_id, ids, metadata=metadata)
        return matched_text

    def _store_embeddings(self, doc_id, entries: List[EmbeddingEntry], *args, **kwargs):
        self.embedding_factory.store(doc_id, entries, *args, **kwargs)

    def _store_text(self, doc_id, entries: List[TextEntry], *args, **kwargs):
        self.document_factory.store(doc_id, entries, *args, **kwargs)


class ChunkingCachingStrategy(CachingStrategy):
    """
    Caching strategy that chunks the document into smaller chunks and caches each chunk separately.
    :parameter chunk_size: The number of sentences per chunk.
    :parameter sentence_word_count: The minimum and maximum word count of a sentence in the document.
    """

    def __init__(self,
                 embedding_factory: EmbeddingFactory,
                 document_factory: DocumentFactory,
                 embedding_operator: EmbeddingOperator,
                 document_operator: DocumentOperator,
                 chunk_size=16,
                 sentence_word_count=(15, 100)):
        super().__init__(embedding_factory, document_factory, embedding_operator, document_operator)
        self.chunk_size = chunk_size
        self.sentence_word_count = sentence_word_count

    def _chunk_corpus(self, corpus: str) -> List[TextEntry]:
        chunks = []
        count_words = lambda sentence: len(sentence.split())
        sentence_acc = ""

        for sentence in corpus.split("."):
            if count_words(sentence_acc) + count_words(sentence) > self.sentence_word_count[1]:
                chunks.append(sentence_acc)
                sentence_acc = ""
            sentence_acc += sentence

        if sentence_acc:
            chunks.append(sentence_acc)

        # now we have a list of chunks, we need to split them into smaller chunks according to chunk_size
        chunked_chunks = []
        for chunk in chunks:
            chunked_chunks += [chunk[i:i + self.chunk_size] for i in range(0, len(chunk), self.chunk_size)]

        text_entry_chunks = []
        for chunk in chunked_chunks:
            chunk_id = generate_id()
            for sentence in chunk:
                txt_entry_id = generate_id()
                text_entry_chunks.append(TextEntry(id=txt_entry_id, text=sentence, metadata={
                    "chunk_id": chunk_id
                }))

        return text_entry_chunks
