# Import the dependecies
import os
import pandas as pd
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import time
import tiktoken
# import openai  as openai_client
from openai import AzureOpenAI
from pymilvus import MilvusClient


tokenizer = tiktoken.get_encoding("cl100k_base")

def embed(text, openai_client, embedding_model):
    if isinstance(text, dict):
        text = list(text.values())
    
    embeddings = openai_client.embeddings.create(
        input=text,
        model=embedding_model
    )
    
    # Extract the embeddings from the response
    if isinstance(embeddings.data, list):
        # Return the embeddings if the response is a list
        return [embedding.embedding for embedding in embeddings.data]
    else:
        # Return the embedding if the response is not a list
        return embeddings.data[0].embedding


def openai_embeddings(url_data, llm_cred, vectordb_cred, openai_client, embed_model):
    # df = pd.DataFrame(columns=['url', 'text', 'embedding', 'n_tokens'])

    # for url, data in url_data.items():
    #     # Embed the data
    embedding = embed(url_data, openai_client, embedding_model=embed_model)
        # n_tokens = len(tokenizer.encode(data))  # Assuming tokenizer is defined somewhere

        # # Append to DataFrame
        # df = df.append({'url': url, 'text': data, 'embedding': embedding, 'n_tokens': n_tokens}, ignore_index=True)
    print("embedding done")
    return embedding



# def openai_embeddings(text_data, file_name, max_tokens, openai_client, embed_model):
#     # print(text_data)

#     tokenizer = tiktoken.get_encoding("cl100k_base")

#     df = pd.DataFrame(columns=['file_name','text', 'n_tokens', 'embedding'])
#     n_tokens=0
#     for text in text_data:
#         # print(text)
      
#         shortened_texts = split_into_many(text,max_tokens)
#         for shortened_text in shortened_texts:
#             print("------")
#             # print(shortened_texts)   
#             embedding = embed(shortened_text, openai_client, embed_model) # You'll need to define or import the embed function
#             df = df._append({'file_name':file_name,'text': shortened_text, 'n_tokens': len(tokenizer.encode(shortened_text)), 'embedding': embedding}, ignore_index=True)
       
#     df.to_csv(file_name, index=False)

#     return df



    


def make_connection(host, port, timeout=30):
    connections.connect(host=host, port=port)
    print('connection established')



def url_exists_in_milvus(collection, url):
    import urllib.parse

    encoded_url = urllib.parse.quote(url)

    expr = f"url:'{encoded_url}'"

    result = collection.query(expr=expr)


    
    if result:
        return True
    else:
        return False





def update_url_data(collection, url, content, embedding, n_tokens):
    query_expression = f"url:'{url}'"
    results = collection.search(expression=query_expression, limit=1)

    if len(results) > 0:
        doc_id = results[0].id
        update_data = {
            "content": content,
            "embedding": embedding,
            "n_tokens": n_tokens
        }
        collection.update(id=doc_id, data=update_data)
    else:
        raise ValueError(f"URL '{url}' not found in the collection.")



def insert_url_data(collection, url, content, embedding, n_tokens):

    url = str(url)
    content = str(content)
    n_tokens = int(n_tokens)
    print("Till here no problem")
    print(type(embedding))
    flattened_embedding = [float(val) for sublist in embedding for val in sublist]
    print("Crossed check point 1")
    
    document = {
        "url": url,
        "content": content,
        "embedding": flattened_embedding,
        "n_tokens": n_tokens
    }
    collection.insert([document])
    print("Inserted in Milvus")






def create_collection(COLLECTION_NAME, DIMENSION):
    if utility.has_collection(COLLECTION_NAME):
        print('existing collection loaded')
        return Collection(COLLECTION_NAME)
    else:
        fields = [
            FieldSchema(name='url', dtype=DataType.VARCHAR, description='URL of the document', is_primary=True, max_length=200),
            FieldSchema(name='content', dtype=DataType.VARCHAR, description='Content of the document', max_length=35000),  # Adjust max_length as needed
            FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Embedding vectors', dim=DIMENSION),
            FieldSchema(name='n_tokens', dtype=DataType.INT64, description='Number of tokens in the content')
        ]
        schema = CollectionSchema(fields=fields, description='Your collection description')
        collection_new = Collection(name=COLLECTION_NAME, schema=schema)
        print('New collection created')

        collection = Collection(COLLECTION_NAME)  # Get the existing collection.
        collection.create_partition("Admin")
        collection.create_partition("System")
        collection.create_partition("User")
        print("Partitions are created")

        index_params = {
            'index_type': 'IVF_FLAT',
            'metric_type': 'L2',
            'params': {'nlist': 1024}
        }
        print('Index creation started')
        collection_new.create_index(field_name="embedding", index_params=index_params)
        print('Index created')
        return collection_new

def openai_embeddings2(url_data, llm_cred, vectordb_cred, openai_client, embed_model):

    embeddings = []
    for url, data in url_data.items():
        embedding = embed([data], openai_client, embedding_model=embed_model)
        embeddings.append(embedding)
    print("embedding done")
    return embeddings


def process_and_store_data(client_id, new_changed_content, llm_cred, vectordb_cred):

    openai_client = AzureOpenAI(api_key=llm_cred["api_key"], 
                     api_version=llm_cred["api_version"], 
                     azure_endpoint=llm_cred["api_base"])
    make_connection(host=vectordb_cred["host_ip"], port=vectordb_cred["host_port"]) #connect with milvus
    collection = create_collection(COLLECTION_NAME=client_id, DIMENSION=llm_cred["embed_dim"])
    
    for item in new_changed_content:
        url = item.get("url")
        content = item.get("content")

        if url is not None and content is not None:
            embedding = openai_embeddings({url: content}, llm_cred, vectordb_cred, openai_client, embed_model=llm_cred["embed_model"])
            print("Embed done")
            n_tokens = len(tokenizer.encode(content))  
            # if len(content)>14999:
            #     pass

            # # Check if the URL already exists in Milvus
            # if url_exists_in_milvus(collection, url):
            #     # Update existing data
            #     update_url_data(collection, url, content, embedding, n_tokens)
            #     print("Updated 1")
            # else:
            insert_url_data(collection, url, content, embedding, n_tokens)
                # print("Inserted 1")
        else:
            print("Skipping item because 'url' or 'content' is missing")

    print("Done here")



# from db_functions import fetch_data_from_db
# client_id = "lama2_vector_d2d786b9_38be_4abe_b22a_ae18446e3e40"
# registrydb_params = {
#     'host': 'genaidbserver.postgres.database.azure.com',
#     'port': 5432,
#     'user': 'ravinder',
#     'password': 'Admin@345',
#     'dbname': 'gen_ai_db'
# }


# result_from_db = fetch_data_from_db(registrydb_params, client_id)
# llm_cred = {
#     "api_base": result_from_db['api_base'],
#     "api_key": result_from_db['api_key'],
#     "api_type": result_from_db['api_type'],
#     "api_version": result_from_db['api_version'],
#     "embed_model": result_from_db['embed_model'],
#     "embed_dim": result_from_db['embed_dim'],
#     "completion_model": result_from_db['completion_model']
# }
# vectordb_cred = {
#     "host_ip": result_from_db['vectordb_host'],
#     "host_port": result_from_db['vectordb_port']
#     }

# import json

# json_file_path = "D:/Work/Genai_Bharani/uploads/ITC_ITCHOTELS/extracted_text/extracted_text_web/textual_data_2024-04-03_16-16-48.json"
# with open(json_file_path, "r") as json_file:
#     new_changed_content = json.load(json_file)
# # D:/Work/Genai_Bharani/uploads/ITC_ITCHOTELS/extracted_text/extracted_text_web/textual_data_2024-04-03_16-16-48.json
# json_file_path = "D:/Work/uploads/demonew_demonew_b34fc66e_c448_4627_baaf_8444b19288cf/extracted_text/extracted_file_text/files_data_2024-04-04_05-36-07.json"
# with open(json_file_path, "r") as json_file:
#     changed_content_files = json.load(json_file)

# if isinstance(changed_content_files, dict) and changed_content_files:
#     new_changed_content.append(changed_content_files)

# df = process_and_store_data(client_id, new_changed_content, llm_cred, vectordb_cred)





