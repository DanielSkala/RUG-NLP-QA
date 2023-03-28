from abc import ABC, abstractmethod
from algorithm.models import Document
from PyPDF2 import PdfReader
from tqdm import tqdm


class DocumentOperator(ABC):
    @abstractmethod
    def parse(self, document, *args, **kwargs) -> any:
        pass


class PDFDocumentOperator(DocumentOperator):
    def parse(self, document, *args, **kwargs) -> any:
        path = document.data
        # print(path)
        reader = PdfReader(path)  # path / ../'Project plan.pdf'
        text = [page.extract_text() for page in tqdm(reader.pages)]
        return text


if __name__ == '__main__':
    operator = PDFDocumentOperator()
    doc = Document(
        id='1',
        data='../Project plan.pdf'
    )
    text = operator.parse(doc)
    print(text)
