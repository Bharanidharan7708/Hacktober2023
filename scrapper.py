from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from pymilvus import connections
from langchain.embeddings.openai import OpenAIEmbeddings
from pymilvus import utility
from pymilvus import Collection
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.storage.storage_context import StorageContext
import textwrap
from llama_index.core.memory import ChatMemoryBuffer


azure_api = "https://sravanakumar13sathish.openai.azure.com/"
api_key = "f93979cbf9894257affd4fee8b4e08fb"
api_version = "2023-03-15-preview"
EMBEDDING_MODEL = "text-embedding-ada-002"
TEXT_COMPLETION_MODEL = 'Policy_GPT'
CHAT_COMPLETION_MODEL = 'gpt-35-turbo'
llm = AzureOpenAI(
    model="gpt-35-turbo",
    deployment_name=CHAT_COMPLETION_MODEL,
    api_key=api_key,
    azure_endpoint=azure_api,
    api_version=api_version,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name=EMBEDDING_MODEL,
    api_key=api_key,
    azure_endpoint=azure_api,
    api_version=api_version,
)
Settings.llm = llm
Settings.embed_model = embed_model

# documents = SimpleDirectoryReader("C:/Users/Lenovo/Desktop/Experiments/Scrapper/test_dir").load_data()
# , dim=1536

vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530', collection_name='ITC_Test' )
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context
# )

# query_engine = index.as_query_engine()
# response = query_engine.query("hotels in jaipur?")
# print(textwrap.fill(str(response), 100))

# chat_memory = ChatMemoryBuffer()

# while True:
#     user_input = input("User: ")
#     if user_input.lower() == "exit":
#         break
    
#     response = llm.complete_prompt(user_input)
#     chat_memory.add_chat(user_input, response.choices[0].text)
#     print("Chatbot:", response.choices[0].text)

# chat_memory.save("chat_memory.txt")


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
# query = "hotels in himachal pradesh"
# query_engine = index.as_query_engine()
# answer = query_engine.query(query)
# print(answer.response)



memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        """You are an ITC hotels chatbot, your task is to answer questions asked by the user regarding the hotels using the data you have been provided.
        If the question asked is not mentioned in the data provided to you, simply mention, I do not know the answer to the question you asked
        If user asks a question not related to ITC hotels, simply mention I do not know the answer to the question you asked """
        
    ),
)

while True:
    text_input = input("User: ")
    if text_input == "exit":
        chat_engine.reset()
        break
    response = chat_engine.chat(text_input)
    print(f"Agent: {response}")
# response = chat_engine.chat("Hi, My name is vaibhav")
# print(response)



    
