# page_converter.py
# from pdf2image import convert_from_path
# import tempfile

# def pdf_to_images(pdf_path: str, dpi: int = 200) -> list:
#     """
#     Converts a PDF into a list of image file paths (one per page).
#     Returns temporary image file paths.
#     """
#     images = convert_from_path(pdf_path, dpi=dpi)
#     temp_image_paths = []

#     for i, image in enumerate(images):
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#         image.save(temp_file.name, "PNG")
#         temp_image_paths.append(temp_file.name)

#     return temp_image_paths


import os
import tempfile
import subprocess
from pdf2image import convert_from_path

def pdf_to_images(file_path: str, dpi: int = 300) -> list:
    """
    Converts a PDF or DOCX file into a list of image file paths (one per page).
    DOCX files are first converted to PDF using LibreOffice.
    Returns temporary image file paths.
    """
    # Check extension
    ext = os.path.splitext(file_path)[1].lower()
    temp_pdf_path = None

    if ext == ".docx":
        # Convert DOCX to PDF
        temp_dir = tempfile.mkdtemp()
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            file_path,
            "--outdir", temp_dir
        ], check=True)

        # Get the converted PDF path
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        temp_pdf_path = os.path.join(temp_dir, f"{base_name}.pdf")
        if not os.path.exists(temp_pdf_path):
            raise FileNotFoundError(f"Failed to convert DOCX to PDF: {temp_pdf_path}")
    elif ext == ".pdf":
        temp_pdf_path = file_path
    else:
        raise ValueError("Unsupported file type. Only .pdf and .docx are supported.")

    # Convert PDF to images
    images = convert_from_path(temp_pdf_path, dpi=dpi)
    temp_image_paths = []

    for i, image in enumerate(images):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file.name, "PNG")
        temp_image_paths.append(temp_file.name)

    return temp_image_paths
