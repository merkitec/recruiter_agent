from application.extract_markdown import ExtractMarkdown
import pymupdf4llm
import pathlib

class PyMuPdf4Llm(ExtractMarkdown):
    def __init__(self):
        super().__init__()

    def extract(self, file_path):
        return pymupdf4llm.to_markdown(file_path)    
        # pathlib.Path("output.md").write_bytes(md_text.encode())