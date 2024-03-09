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
from llama_index.core import GPTVectorStoreIndex
import new


azure_api = "https://sravanakumar13sathish.openai.azure.com/"
api_key = "f93979cbf9894257affd4fee8b4e08fb"
api_version = "2023-03-15-preview"
EMBEDDING_MODEL = "text-embedding-ada-002"
TEXT_COMPLETION_MODEL = 'Policy_GPT'
CHAT_COMPLETION_MODEL = 'gpt-35-turbo-16k'
llm = AzureOpenAI(
    model="gpt-35-turbo-16k",
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

# GPTVectorStoreIndex
# documents = SimpleDirectoryReader("C:/Users/vaibhavg/Desktop/llamaindex/dataset1").load_data()
# vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530', collection_name='ITC_Chatbot1', dim=1536 )
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# index = GPTVectorStoreIndex.from_documents(
#     documents, storage_context=storage_context)

#default reader
# documents = SimpleDirectoryReader("C:/Users/vaibhavg/Desktop/llamaindex/dataset1").load_data()
# # # service_context = ServiceContext.from_defaults(   chunk_size=512, chunk_overlap=50)
# # # index = VectorStoreIndex.from_documents(   documents, service_context=service_context)

# vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530', collection_name='ITC_Chatbot', dim=1536 ,overwrite = True)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context)
def chatbot(text_input,history):
    vector_store = MilvusVectorStore(uri='http://20.244.48.175:19530', collection_name='ITC_Chatbot')
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    # index = GPTVectorStoreIndex.from_vector_store(vector_store=vector_store)

    memory = ChatMemoryBuffer.from_defaults(token_limit=9000)

    chat_engine = index.as_chat_engine(
        similarity_top_k=8,
        chat_mode="context",
        memory=memory,
        system_prompt=(
            """You are an ITC hotels chatbot, your task is to answer questions asked by the user regarding the hotels using the data you have been provided.
            If the question asked is not mentioned in the data provided to you, simply mention, I do not know the answer to the question you asked
            If user asks a question not related to ITC hotels, simply mention I do not know the answer to the question you asked
            """
            # """You are an ITC hotels chatbot, your task is to answer questions asked by the user regarding the ITC Rajputana hotel,Jaipur using the data you have been provided.
            # If the question asked is not mentioned in the data provided to you, simply mention, I do not know the answer to the question you asked
            # If user asks a question not related to ITC hotels, simply mention I do not know the answer to the question you asked """
            
        ),
    )

    detected_lang = new.detect(text_input)

    if (detected_lang != 'en'):
        text_input_temp = new.translate(text_input, 'en') #to translate the user input to english
        if not history:
            history = new.city(text_input_temp)
        if history[0] == 'Jaipur':
            context = "ITC Rajputana, Jaipur"
        elif history[0] == 'Vellore':
            context = "Fortune Park, Vellore"
        elif history[0] == 'Agra':
            context = "ITC Mughal, Agra"
        else:
            context = "ITC hotels"

        context = new.translate(context, detected_lang) #here we're translating the context to user language

    else:
        if not history:
            history = new.city(text_input_temp)
        if history[0] == 'Jaipur':
            context = "ITC Rajputana, Jaipur"
        elif history[0] == 'Vellore':
            context = "Fortune Park, Vellore"
        elif history[0] == 'Agra':
            context = "ITC Mughal, Agra"
        else:
            context = "ITC hotels"

        
    text_input = text_input + '?'
    # print("||",history,context)
    # chat_engine.reset()
    response = chat_engine.chat(context) 
    response = chat_engine.chat(text_input)
    # for message in chat_engine.chat_history:
    #     print(f"{message.role}: {message.content}") 
    chat_engine.reset()
    return [response,history]


history=[]
text_input = "I am going to Jaipur "
resp = chatbot(text_input,history)
print(resp[0])
# history=['Jaipur']
# text_input = "rooms"
# resp = chatbot(text_input,history)
# print(resp[0])



# history=['Vellore']
# text_input = "Operational Period: all day"
# resp = chatbot(text_input,history)
# print(resp[0])
# Operational Period:

        # for message in chat_engine.chat_history:
        #     print(f"{message.role}: {message.content}")
    

 
