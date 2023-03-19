from abc import ABC, abstractmethod
from algorithm.models import Document, TextEntry


class DocumentOperator(ABC):
    @abstractmethod
    def parse(self, document, *args, **kwargs) -> any:
        pass

    @abstractmethod
    def store(self, entries: [TextEntry], *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def retrieve(self, document_ids: [int], *args, **kwargs) -> [TextEntry]:
        pass


class PDFDocumentOperator(DocumentOperator):
    def parse(self, document, *args, **kwargs) -> any:
        data = document.data

    def store(self, entries: [TextEntry], *args, **kwargs) -> bool:
        pass

    def retrieve(self, document_ids: [int], *args, **kwargs) -> [TextEntry]:
        pass
