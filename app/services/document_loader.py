from langchain_text_splitters import RecursiveCharacterTextSplitter
 
from pypdf import PdfReader #the PDF-reading tool


def extract_text_from_pdf(file_path: str) -> str: #function to extract PDF text
    """
    Extract text from a PDF
    """

    reader = PdfReader(file_path)

    extracted_text = "" #empty box to collect text

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or "" #If the page has no text, return an empty string

        extracted_text += f"\n--- Page {page_number} ---\n"
        extracted_text += page_text

    return extracted_text


def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    return chunks


