"""Concrete creators that produce specific document types."""

from creator import DocumentCreator
from concrete_products import PDFDocument, WordDocument, ExcelDocument


class PDFCreator(DocumentCreator):
    def factory_method(self):
        return PDFDocument()


class WordCreator(DocumentCreator):
    def factory_method(self):
        return WordDocument()


class ExcelCreator(DocumentCreator):
    def factory_method(self):
        return ExcelDocument()
