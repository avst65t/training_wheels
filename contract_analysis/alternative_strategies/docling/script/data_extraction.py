from docling.document_converter import DocumentConverter

def parse_document_with_docling(file_path: str):
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()
