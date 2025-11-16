# service.py
import os
from page_converter import pdf_to_images
from parallel_processor import extract_data_from_pages_parallel_sync
from post_process import merge_field_outputs

def analyze_and_store_multimodal(file_path: str) -> dict:
    print('Converting PDF to images...')
    image_paths = pdf_to_images(file_path)
    print(f'Converted {len(image_paths)} pages to images.')

    print('Sending images in parallel to GPT API...')
    results = extract_data_from_pages_parallel_sync(image_paths)
    print('Extraction complete.', results)

    print('Merging results from all pages...')
    merged = merge_field_outputs(results)
    print('Fields merged, JSON output ready.', merged)

    # Clean up temporary images
    for path in image_paths:
        try:
            print('removing: ', path)
            os.remove(path)
        except Exception as e:
            print(f"Warning: Could not delete temporary image {path}: {e}")

    return merged
