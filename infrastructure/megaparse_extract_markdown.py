from megaparse import MegaParse
from langchain_openai import ChatOpenAI
from megaparse.parser.unstructured_parser import UnstructuredParser

from application.extract_markdown import ExtractMarkdown

class MegaParseExtractMarkdown(ExtractMarkdown):
    def __init__(self):
        super().__init__()

    def extract(self, file_path) -> str:
        parser = UnstructuredParser()
        megaparse = MegaParse(parser)
        response = megaparse.load(file_path)
        # print(response)
        megaparse.save("./test.md")
        return response
