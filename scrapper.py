[2:21 PM] Vaibhav Achar (IN)
from llama_index.llms.azure_openai import AzureOpenAI
 
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
 
import logging
 
import sys
 
from llama_index.core import Settings
 
from llama_index.vector_stores.milvus import MilvusVectorStore
 
 
from llama_index.core.storage.chat_store import SimpleChatStore
 
from llama_index.core.memory import ChatMemoryBuffer
 
from pymilvus import connections
from langchain.embeddings.openai import OpenAIEmbeddings
 
 
# from pymilvus import utility
 
# from pymilvus import Collection
 
 
# connections.connect(          #to connect with db
 
#     host='20.244.48.175',
 
#     port='19530'
 
# )
 
 
logging.basicConfig(
 
    stream=sys.stdout, level=logging.INFO
 
)  # logging.DEBUG for more verbose output
 
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
 
 
azure_api = "https://sravanakumar13sathish.openai.azure.com/"
 
OPENAI_API_KEY = "f93979cbf9894257affd4fee8b4e08fb"
 
api_version = "2023-03-15-preview"
 
EMBEDDING_MODEL = "text-embedding-ada-002"
 
TEXT_COMPLETION_MODEL = 'Policy_GPT'
 
CHAT_COMPLETION_MODEL = 'gpt-35-turbo'
 
 
llm = AzureOpenAI(
 
    model="gpt-35-turbo",
 
    deployment_name=CHAT_COMPLETION_MODEL,
 
    api_key=OPENAI_API_KEY,
 
    azure_endpoint=azure_api,
 
    api_version=api_version,
 
)
 
# You need to deploy your own embedding model as well as your own chat completion model
 
embeddings = OpenAIEmbeddings(
 
        deployment=EMBEDDING_MODEL,
 
        model="text-embedding-ada-002",
 
        openai_api_base=OPENAI_API_KEY,
 
        openai_api_type="azure",
 
        chunk_size=1
 
    )
 
Settings.llm = llm
 
Settings.embed_model = embeddings
 
##MILVUS
 
vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530',
 
                                 collection_name='ITC_ITCHOTELS_scrapped')
 
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
 
 
# chat_store = SimpleChatStore()
 
# chat_memory = ChatMemoryBuffer.from_defaults(
 
#     token_limit=3000,
 
#     chat_store=chat_store,
 
#     chat_store_key="user1",
 
# )
 
 
def search_and_query(collection, search_vectors, search_field, search_params):
 
    collection.load()
 
    result = collection.search(search_vectors, search_field, search_params, limit=5, output_fields=["id", "text"])
 
    return result
 
query = "I want the most luxurious and grandest hotel in chennai"
 
query_vector = embeddings.embed_query(query)
 
result = search_and_query(vector_store, [query_vector], "embedding", {"metric_type": "L2", "params": {"nprobe": 10}})
 
print(result)
