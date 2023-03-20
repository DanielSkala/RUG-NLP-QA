from abc import ABC, abstractmethod
from algorithm.models import TextEntry
from PyPDF2 import PdfReader
from tqdm import tqdm
import pickle


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
        reader = PdfReader(data)
        text = [page.extract_text() for page in tqdm(reader.pages)]
        return text

    def store(self, entries: [TextEntry], *args, **kwargs) -> bool:
        try:
            with open("entries.pkl", "wb") as f:
                pickle.dump(entries, f)
            return True
        except Exception as e:
            print(e)
            return False

    def retrieve(self, document_ids: [int], *args, **kwargs) -> [TextEntry]:
        try:
            with open("entries.pkl", "rb") as f:
                entries = pickle.load(f)
            return entries
        except Exception as e:
            print(e)
            return None
