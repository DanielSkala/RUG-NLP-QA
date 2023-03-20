from abc import ABC, abstractmethod
from algorithm.models import TextEntry
from PyPDF2 import PdfReader
from tqdm import tqdm
import pickle


class DocumentOperator(ABC):
    @abstractmethod
    def parse(self, document, *args, **kwargs) -> any:
        pass


class PDFDocumentOperator(DocumentOperator):
    def parse(self, document, *args, **kwargs) -> any:
        data = document.data
        reader = PdfReader(data)
        text = [page.extract_text() for page in tqdm(reader.pages)]
        return text
