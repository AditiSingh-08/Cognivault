# import re
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from pypdf import PdfReader
# import os

# def clean_text(text: str) -> str:
#     # Replace multiple spaces or tabs with a single space
#     text = re.sub(r"[ \t]+", " ", text)

    
#     lines = [line.strip() for line in text.splitlines()]

#     # Preserve paragraph breaks while removing excessive blank lines
#     text = "\n".join(lines)
#     text = re.sub(r"\n{3,}", "\n\n", text)

#     return text.strip()

# def extract_text_from_pdf(file_path: str) -> list[dict]:

#     reader = PdfReader(file_path)
#     extracted_pages = []

#     for page_number, page in enumerate(reader.pages, start=1):
#         page_text = page.extract_text(extraction_mode="layout") or ""
#         page_text = clean_text(page_text)
#         extracted_pages.append({
#             "text": page_text,
#             "metadata": {
#                 "source": os.path.basename(file_path),
#                 "page": page_number
#             }
#         })

#     return extracted_pages


# def split_text_into_chunks(
#     pages: list[dict],
#     chunk_size: int = 500,
#     chunk_overlap: int = 50
# ) -> list[dict]:

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         separators=["\n\n", "\n", " ", ""]
#     )

#     all_chunks = []

#     for page in pages:
#         chunks = splitter.split_text(page["text"])

#         for chunk_number, chunk in enumerate(chunks):
#             all_chunks.append({
#                 "text": chunk,
#                 "metadata": {
#                     **page["metadata"],
#                     "chunk": chunk_number
#                 }
#             })

#     return all_chunks

import re
import os
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)

    lines = [line.strip() for line in text.splitlines()]

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_path: str) -> list[dict]:

    extracted_pages = []

    with pymupdf.open(file_path) as doc:

        for page_number, page in enumerate(doc, start=1):

            page_text = page.get_text("text", sort=True) or ""
            page_text = clean_text(page_text)

            extracted_pages.append({
                "text": page_text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": page_number
                }
            })

    return extracted_pages


def split_text_into_chunks(
    pages: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk_number, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "metadata": {
                    **page["metadata"],
                    "chunk": chunk_number
                }
            })

    return all_chunks
