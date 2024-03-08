from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.storage.storage_context import StorageContext
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI  # Import OpenAI LLM
from llama_index.core.query_engine import SubQuestionQueryEngine
import textwrap
 
# Azure OpenAI configurations
azure_api = "https://sravanakumar13sathish.openai.azure.com/"
api_key = "f93979cbf9894257affd4fee8b4e08fb"
api_version = "2023-03-15-preview"
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_COMPLETION_MODEL = 'gpt-35-turbo'
 
# Initialize Azure OpenAI models
llm = AzureOpenAI(
    model=CHAT_COMPLETION_MODEL,
    deployment_name=CHAT_COMPLETION_MODEL,
    api_key=api_key,
    azure_endpoint=azure_api,
    api_version=api_version,
)
 
embed_model = AzureOpenAIEmbedding(
    model=EMBEDDING_MODEL,
    deployment_name=EMBEDDING_MODEL,
    api_key=api_key,
    azure_endpoint=azure_api,
    api_version=api_version,
)
 
# Set Azure OpenAI models in settings
Settings.llm = llm
Settings.embed_model = embed_model
 
# Load documents
documents = SimpleDirectoryReader("C:/Users/azureuser/Desktop/Llamaindex/Text_File").load_data()
 
# Create Milvus vector store
vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530', collection_name='ITC_Test', dim=1536)
 
# Create storage context and index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
 
individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index.as_query_engine(),
        metadata=ToolMetadata(
            name="itc_hotels",
            description="Useful for answering queries about ITC hotels.",
        ),
    )
]
 
# Define your query engine with the OpenAI LLM
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=individual_query_engine_tools,
    llm=OpenAI(model="gpt-3.5-turbo"),  # Assuming you have the OpenAI LLM configured
)
 
# Create tools for OpenAIAgent
 
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description="You are an ITC Bot answering questions related to hotels, booking, amenities queries",
    ),
)
tools = individual_query_engine_tools + [query_engine_tool]
 
# Create a ChatStore
chat_store = SimpleChatStore()
 
# Create a ChatMemoryBuffer using the ChatStore
chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
 
# Create an OpenAIAgent from the tools
agent = OpenAIAgent.from_tools( query_engine=query_engine)
 
# Interactive chat loop
while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = agent.chat(text_input)
    print(f"Agent: {response}")
