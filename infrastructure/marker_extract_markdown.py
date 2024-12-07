from application.extract_markdown import ExtractMarkdown

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

class MarkerExtractMarkdown(ExtractMarkdown):
    def __init__(self):
        super().__init__()

    def extract(self, file_path) -> str:
        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(file_path)
        text, _, images = text_from_rendered(rendered)
        return text
