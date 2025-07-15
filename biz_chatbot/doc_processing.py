import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.storage.storage_context import StorageContext
from config import DATA_DIR, INDEX_DIR, OPENAI_API_KEY

os.makedirs(INDEX_DIR, exist_ok=True)

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

def build_index(k_base_name):
    print(f"\nLoading documents from {DATA_DIR}/{k_base_name}")
    documents = SimpleDirectoryReader(f"{DATA_DIR}/{k_base_name}").load_data()
    Settings.chunk_size = 1024
    Settings.chunk_overlap = 256

    db = chromadb.PersistentClient(path=INDEX_DIR)
    chroma_collection = db.get_or_create_collection(k_base_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context)

    print(f"{k_base_name} Index successfully built and saved.")
