import openai
from langchain.text_splitter import TokenTextSplitter
 
azure_api = "https://sravanakumar13sathish.openai.azure.com/"
api_key = "f93979cbf9894257affd4fee8b4e08fb"
api_version = "2023-03-15-preview"
EMBEDDING_MODEL = "text-embedding-ada-002"
TEXT_COMPLETION_MODEL = 'Policy_GPT'
CHAT_COMPLETION_MODEL = 'gpt-35-turbo'
openai.api_base = azure_api
openai.api_key = api_key
openai.api_type = 'azure'
openai.api_version = api_version
 
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = azure_api
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_VERSION"] = api_version
 
   embeddings = OpenAIEmbeddings(
            deployment=EMBEDDING_MODEL,
            model="text-embedding-ada-002",
            openai_api_base=azure_api,
            openai_api_type="azure",
            chunk_size=1
        )
