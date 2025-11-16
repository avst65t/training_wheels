# utils/pdf_utils.py

from pdf2image import convert_from_path
import os
from uuid import uuid4
from typing import List

def convert_pdf_to_images(pdf_path: str, output_dir: str = "temp_images") -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=200)

    image_paths = []
    for i, img in enumerate(images):
        filename = f"{uuid4().hex}_page_{i+1}.png"
        full_path = os.path.join(output_dir, filename)
        img.save(full_path, "PNG")
        image_paths.append(full_path)

    return image_paths
    