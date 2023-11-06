import os
import logging
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, OpenAIEmbedding, StorageContext, load_index_from_storage
import json
from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
import gradio as gr

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("OPENAI_API_KEY not found in environment variables.")
    exit(1)

# # Create a ServiceContext
# service_context = ServiceContext.from_defaults(
#     llm= OpenAI(model='gpt-3.5-turbo'),
#     embed_model= OpenAIEmbedding(),
#     node_parser= SimpleNodeParser.from_defaults(
#     text_splitter=TokenTextSplitter(chunk_size=1024, chunk_overlap=20)),
#     chunk_size=1024
# )

# Initialize VectorStoreIndex and load or create index
# def construct_index(directory_path):
#     try:        
#         storage_context = StorageContext.from_defaults(persist_dir="./storage")
#         index = load_index_from_storage(storage_context)
#     except:
#         documents = SimpleDirectoryReader(directory_path).load_data()
#         index = VectorStoreIndex.from_documents(documents, service_context=service_context)
#         index.storage_context.persist()
#     return index

# index = construct_index("html_downloads")

# # Define queries and get responses from the chatbot using the context information
# queries = [
#     # "What meals are provided during explore?",
#     # "What is Tanzu?",
#     "Give me information about this session: Analyzing Horizon User Experience Using Free Tools on VMware TestDrive [EUSB2093BCN]"
#     # Add more queries as needed
# ]
# for query in queries:
#     query_engine = index.as_query_engine()
#     response = query_engine.query(query)
#     logging.info(f"Query: {query}\nResponse: {response}")


def construct_index():
    index = None
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    except:
        print("The storage context didn't load correctly")
        exit
    return index
def chatbot(input_text):
    global service_context
    global openai
    os.environ['OPENAI_API_KEY'] = api_key
    openai.api_key = api_key
    index.service_context = ServiceContext.from_defaults(
    llm= OpenAI(model='gpt-3.5-turbo'),
    embed_model= OpenAIEmbedding(),
    node_parser= SimpleNodeParser.from_defaults(
    text_splitter=TokenTextSplitter(chunk_size=1024, chunk_overlap=20)),
    chunk_size=1024
)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    print("Response:", response.response)
    try:
        json.loads(response.response)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
    return response.response


index = construct_index()
iface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.inputs.Textbox(lines=7, label="How may I help you?")
    ],
    outputs="text",
    title="Tanzu-Trained-ChatBot",
)

iface.launch(debug=True, server_name="0.0.0.0")