from pathlib import Path
import hashlib

from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:
    """
    Loads enterprise PDF documents and generates
    a unique hash for duplicate detection.
    """

    def load_pdf(self, pdf_path: str):
        """
        Load PDF and return LangChain Documents.
        Each page is returned as a separate Document object.
        """

        pdf_path = Path(pdf_path).resolve()

        if not pdf_path.exists():
            raise FileNotFoundError(f"{pdf_path} not found.")

        loader = PyPDFLoader(str(pdf_path))

        documents = loader.load()

        document_name = pdf_path.name

        for page_no, doc in enumerate(documents):

            doc.metadata["document_name"] = document_name
            doc.metadata["page"] = page_no + 1
            doc.metadata["source"] = str(pdf_path)

        return documents

    def generate_document_hash(self, pdf_path: str):
        """
        Generate SHA-256 hash of the PDF.
        Used to prevent duplicate uploads.
        """

        pdf_path = Path(pdf_path).resolve()

        sha256 = hashlib.sha256()

        with open(pdf_path, "rb") as file:

            while True:

                chunk = file.read(4096)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()
