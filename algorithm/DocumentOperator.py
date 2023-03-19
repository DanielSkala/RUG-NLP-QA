import PyPDF2
import uuid
import tqdm


class DocumentOperator:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.doc_id = uuid.uuid4()
        self.data = self.parse()

    def parse(self):
        data = []
        with open(self.pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in tqdm.tqdm(range(len(pdf_reader.pages))):
                text = pdf_reader.pages[page_num].extract_text()
                data.append(text)

        return data


if __name__ == '__main__':
    pdf_file = '../book.pdf'
    document_operator = DocumentOperator(pdf_file)
    parsed_document = document_operator.parse()

    print('Doc ID:', document_operator.doc_id)
    # print('Data:', document_operator.data)
    print('Length:', len(document_operator.data))
