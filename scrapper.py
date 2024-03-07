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
# from pymilvus import utility
# from pymilvus import Collection
 
 
connections.connect(          #to connect with db
    host='20.244.48.175',
    port='19530'
)
 
 
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
 
 
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
 
# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name=EMBEDDING_MODEL,
    api_key=api_key,
    azure_endpoint=azure_api,
    api_version=api_version,
)
Settings.llm = llm
Settings.embed_model = embed_model
 
##MILVUS
vector_store = MilvusVectorStore(host='20.244.48.175',
                                 port='19530',
                                 collection_name='ITC_ITCHOTELS_scrapped')
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
 
 
# chat_store = SimpleChatStore()
 
# chat_memory = ChatMemoryBuffer.from_defaults(
#     token_limit=3000,
#     chat_store=chat_store,
#     chat_store_key="user1",
# )
 
query = "How many opulent rooms and suits are present in the ITC Mughal hotel"
query_engine = index.as_query_engine()
answer = query_engine.query(query)
print(answer)
