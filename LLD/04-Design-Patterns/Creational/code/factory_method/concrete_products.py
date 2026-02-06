"""Concrete document products."""

from product import Document


class PDFDocument(Document):
    def create(self) -> str:
        return "PDF document created with text layout engine"

    def save(self, filename: str) -> str:
        return f"Saved as {filename}.pdf"

    def get_extension(self) -> str:
        return ".pdf"


class WordDocument(Document):
    def create(self) -> str:
        return "Word document created with rich text formatting"

    def save(self, filename: str) -> str:
        return f"Saved as {filename}.docx"

    def get_extension(self) -> str:
        return ".docx"


class ExcelDocument(Document):
    def create(self) -> str:
        return "Excel spreadsheet created with grid layout"

    def save(self, filename: str) -> str:
        return f"Saved as {filename}.xlsx"

    def get_extension(self) -> str:
        return ".xlsx"
