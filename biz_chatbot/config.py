import os
from dotenv import load_dotenv

# BASE_URL = "https://biztecno.net/"
DATA_DIR = "scraped_sites"
INDEX_DIR = "chroma_index"
# COLLECTION_NAME = "biztecno_docs"

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
