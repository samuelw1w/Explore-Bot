import os
import logging
from llama_index import GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader, StorageContext, LLMPredictor, load_index_from_storage
#from llama_index.node_parser import SimpleNodeParser
#from langchain.chat_models import ChatOpenAI
from llama_index.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
os.environ['OPENAI_API_KEY'] = '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'

# Load OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("OPENAI_API_KEY not found in environment variables.")
    exit(1)

# Initialize LLM Predictor
OpenAI.api_key = api_key
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", streaming=True))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size=512)

# Initialize storage context and load or create index
def construct_index(directory_path):
    try:        
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    except:
        documents = SimpleDirectoryReader('html_downloads').load_data()
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist()
    return index

index = construct_index("html_downloads")

# Define queries and get responses from the chatbot using the context information
queries = [
    "What is Tanzu Application Platform",
    "What are some Activities I can do?"
    # Add more queries as needed
]
for query in queries:
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    logging.info(f"Query: {query}\nResponse: {response}")


