import chromadb
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatSummaryMemoryBuffer
from config import INDEX_DIR, OPENAI_API_KEY
from prompt import openai_template_str

def run_chatbot(k_base_name):
    print("\nInitializing the BizBot...")

    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
    Settings.llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0)

    chroma_client = chromadb.PersistentClient(path=INDEX_DIR)
    chroma_collection = chroma_client.get_or_create_collection(k_base_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store)

    openai_template = PromptTemplate(openai_template_str)

    memory = ChatSummaryMemoryBuffer.from_defaults(llm=Settings.llm, token_limit=5000)

    query_engine = index.as_query_engine(
        # chat_mode="condense_plus_context",
        memory=memory,
        text_qa_template=openai_template,
        streaming=True,
        similarity_top_k=10
    )

    print("BizBot is ready. Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("\nExiting. Have a nice day!")
            break
        
        response = query_engine.query(query)
        print(f"BizBot: ", end='', flush=True)
        response.print_response_stream()
        # for token in response.response_gen:
        #     print(token, end="", flush=True)
        
        print('\n\n')