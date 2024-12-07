from abc import ABC, abstractmethod

class ExtractMarkdown(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> str:
        pass