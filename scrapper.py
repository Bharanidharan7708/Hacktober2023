# Import the dependecies
from flask import Flask, request, jsonify
from db_functions import save_data_to_db, fetch_data_from_db, fetch_all_projects, save_client_details_to_db
from db_functions import update_docu_srcapping,update_docu_storing, update_web_scrapping, update_web_storing
from db_functions import add_docu_name,add_url_name
from save_functions import create_folder_structure, save_url, save_audio, save_image,  save_text_to_file, save_document, save_text_to_file  #scrape_website,
from scrape import read_file
from vectordb import process_and_dump_openai, final_search
from flask_cors import CORS, cross_origin
from pymilvus import  connections,Collection
import time
import json
import ast
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from werkzeug.exceptions import abort
from webscrapper import scrape_website, scrape_website_files
import uuid
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime
from milvus_storage import process_and_store_data
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()




# PostgreSQL database connection parameters for store client details
registrydb_params = {
    'host': 'genaidbserver.postgres.database.azure.com',
    'port': 5432,
    'user': 'ravinder',
    'password': 'Admin@345',
    'dbname': 'gen_ai_db'
}

# max token size for chunking
chunk_max_token = 500

# laoding time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)


# Instantiate the flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



# Endpoint for homepage
@app.route('/', methods=['GET'])
@cross_origin()
def deployedTest():
    return jsonify({'status': 'success', 'message': f"Application loaded successfully at {current_time}."})



# endpoint for creating new entry in DB
@app.route('/create_new', methods=['POST'])
@cross_origin()
def create_new():
    data = request.json

    client_cred = data.get('client_cred','')

    # client_id = save_client_details_to_db(client_cred, registrydb_params)
    client_id_unique = "ITC_ITCHOTELS"
    global client_path
    client_path = create_folder_structure(client_id_unique)
    print(client_path)

    return(jsonify({'status': 'success', 'message': 'Data saved successfully', 'client_id':client_id_unique}))







# endpoint for submitting data
@app.route('/submit_data', methods=['POST'])
@cross_origin()
def submit_data():
    data = request.json

    client_id = data.get('client_id','')
    # client_cred = data.get('client_cred','')
    llm_cred = data.get('llm_cred')
    vectordb_cred = data.get('vectordb_cred')
    rdb_cred = data.get('rdb_cred')
    upload_flag = data.get('upload_flag')
    # unique_id = uuid.uuid4()
    # print(unique_id)
    # print(type(unique_id))
    # client_id = client_cred["client_name"]+"_"+client_cred["project_name"]+"_"+str(unique_id)

    client_id = save_data_to_db(  client_id,llm_cred,vectordb_cred,rdb_cred,  registrydb_params,  upload_flag   )  # lter change the registry db details
    # client_id = client_cred["client_name"]+"_"+client_cred["project_name"]
 
    return(jsonify({'status': 'success', 'message': 'Data saved successfully'}))







#endpoint for fetching alll project data to list the details
@app.route('/fetch_project_data', methods=['GET'])
@cross_origin()
def fetch_project_data():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5) )  

    # Filtering parameters
    filter_value = request.args.get('filter_value', None)

    # Sorting parameters
    sort_by = request.args.get('sort_by', 'id')  # Default sorting by id
    sort_order = request.args.get('sort_order', 'DESC')  # Default sorting order is descending    

    fetch_result = fetch_all_projects(registrydb_params, page, per_page, sort_by, sort_order, filter_value)

    # print(fetch_result)

    if fetch_result["status"]=="failed":
        return jsonify(fetch_result), 500       
    else:
        return jsonify( { "data":fetch_result["result"]["data"],  "pagination": fetch_result["result"]["pagination_details"] } )



#endpoint for fetching project speciic details
@app.route('/fetch_data/<client_id>', methods=['GET'])
@cross_origin()
def fetch_data(client_id):
    data = fetch_data_from_db(registrydb_params, client_id)
    # print(data)

    if data:
        return jsonify({'status': 'success', 'data': data})
    else:
        return jsonify({'status': 'error', 'message': 'Client not found'})

 


# #endpoint to handle scraping from URL
# @app.route('/upload_urls', methods=['POST'])
# @cross_origin()
# def upload_urls():
#     data = request.json
#     # client_cred = data.get('client_cred','')
#     # llm_cred = data.get('llm_cred')
#     # vectordb_cred = data.get('vectordb_cred')
#     # rdb_cred = data.get('rdb_cred')

#     client_id = data.get('client_id')

#     urls = data.get('urls','')
#     max_depth = data.get('max_depth',)

#     result_from_db = fetch_data_from_db(registrydb_params,client_id)
#     llm_cred = {
#         "api_base":result_from_db['api_base'],
#         "api_key":result_from_db['api_key'],
#         "api_type":result_from_db['api_type'],
#         "api_version":result_from_db['api_version'],
#         "embed_model":result_from_db['embed_model'],
#         "embed_dim":result_from_db['embed_dim'],
#         "completion_model":result_from_db['completion_model']
#         }
#     vectordb_cred = {
#         "host_ip":result_from_db['vectordb_host'],
#         "host_port":result_from_db['vectordb_port']}


    
#     # client_id = client_cred["client_name"]+"_"+client_cred["project_name"]

#     # print(data)
#     # print(data['urls'],"1")
#     # Check if the 'urls' key is present in the data
#     # if 'urls' in data:
        
#     #     urls = ''
#     # else:
#     #     urls = ''
#     # print(data['urls'],"2")
#     # Save data to the 
    
#     # if isinstance(urls, list) and all(isinstance(url, str) for url in urls) and urls:
#         # Save data to the database

#     # # Scrape website and get the result
#     # scraped_data1= scrape_website(client_id, urls)
#     # print(type(scraped_data1))
#     # print(len(scraped_data1))
#     # update_web_scrapping(registrydb_params,client_id)
#     # scraped_data=" ".join(scraped_data1)
#     # print(type(scraped_data))
#     # print(len(scraped_data))
#     # # concatenated_text = '\n'.join(scraped_data)
#     # # milvus_collection_name = client_id
#     # # milvus_dimension = 1536
#     # result_df = process_and_dump_openai(client_id, scraped_data, chunk_max_token, llm_cred, vectordb_cred)
#     # update_web_storing(registrydb_params,client_id)

#     # return jsonify({'status': 'success', 'message': 'Data saved successfully', 'client_id': client_id, 'scraped_data': scraped_data,  'milvus_data': result_df.to_dict(orient='records')})

#     return_text_content = []
#     return_df = []
#     list_length = len(urls)

#     for index,url in enumerate( urls):
#         scrapped_text1, link_status = scrape_website( url, max_depth,client_id,)
#         print(type(scrapped_text1))
#         print(len(scrapped_text1))
#         print(scrapped_text1)
#         print(link_status)
#         scrapped_text=" ".join(scrapped_text1)
#         # print(type(scrapped_text))
#         # print(len(scrapped_text))
#         for url_name in link_status['link_success']:
#             add_url_name(registrydb_params,client_id, url_name, status="success" )
#         for url_name in link_status['link_failure']:
#             add_url_name(registrydb_params,client_id, url_name, status="failed" )

#         if index == list_length - 1:
#             update_web_scrapping(registrydb_params,client_id)
#         # save_text_to_file(client_id, 'url', 'extracted_text'+url, scrapped_text)

#         df = process_and_dump_openai(client_id, scrapped_text, chunk_max_token, llm_cred, vectordb_cred)
#         if index == list_length - 1:
#             update_web_storing(registrydb_params,client_id)       
#         return_text_content.append(scrapped_text)
#         return_df.append(df.to_dict(orient='records'))

#         # save_url(client_name, url)


#     return jsonify({'status': 'success', 'message': 'URL uploaded successfully, Scraping Started for frequency every {frequency}', 'client_id': client_id, 'scraped_data': return_text_content,  'milvus_data': return_df})
    
#     # for index,url in enumerate( urls):
#     #     scrapped_text1, link_status = scrape_website( url, max_depth,client_id,frequency='minute')
#     # print("Storing...")
#     # return {"a":""}


#endpoint to handle scraping from URL

scheduler = BackgroundScheduler(max_instances=5)
scheduler.start()


def process_urls(client_id, urls, max_depth):

    with app.app_context():  # Create application context
        results = []
        return_text_content = []
        return_df = []
        visited_urls = set()
        list_length = len(urls)


        result_from_db = fetch_data_from_db(registrydb_params, client_id)
        llm_cred = {
            "api_base": result_from_db['api_base'],
            "api_key": result_from_db['api_key'],
            "api_type": result_from_db['api_type'],
            "api_version": result_from_db['api_version'],
            "embed_model": result_from_db['embed_model'],
            "embed_dim": result_from_db['embed_dim'],
            "completion_model": result_from_db['completion_model']
        }
        vectordb_cred = {
            "host_ip": result_from_db['vectordb_host'],
            "host_port": result_from_db['vectordb_port']
         }

        for index, url in enumerate(urls):
            if url not in visited_urls:
                print("Scrapping for Client ID:", client_id)
                print('Scrapping for URL:', url)
                current_dir = os.getcwd()
                client_path = os.path.join(current_dir, "uploads", client_id)
                scrapped_text1, link_status_urls, new_changed_content,  scrapped_text2, changed_content_files = scrape_website(url, max_depth, client_id,
                                                                                                    client_path)
                print("Done...")
                print("Length of Changed Json Data:", len(new_changed_content))

                text_data = ""
                if isinstance(new_changed_content, dict):
                    for url, content in new_changed_content.items():
                        text_data += content
                elif isinstance(new_changed_content, list):
                    for content in new_changed_content:
                        text_data += content
                else:
                    print("Unsupported type for web_text:", type(new_changed_content))


                if isinstance(changed_content_files, dict):
                    for url, data in changed_content_files.items():
                        text_data += data
                elif isinstance(changed_content_files, list):
                    for data in changed_content_files:
                        text_data += data
                else:
                    print("Unsupported type for web_file:", type(changed_content_files))

                visited_urls.add(url)
            
            for url_name in link_status_urls['link_success']:
                add_url_name(registrydb_params,client_id, url_name, status="success" )
            for url_name in link_status_urls['link_failure']:
                add_url_name(registrydb_params,client_id, url_name, status="failed" )

            if index == list_length - 1:
                update_web_scrapping(registrydb_params,client_id)
            # save_text_to_file(client_id, 'url', 'extracted_text'+url, scrapped_text)
            # client_id, new_changed_content, changed_content_files, llm_cred, vectordb_cred
            print("Length of new_changed_content:", len(new_changed_content))
            print("Length of changed_content_files:", len(changed_content_files))
            if isinstance(changed_content_files, dict) and changed_content_files:
                new_changed_content.append(changed_content_files)
            df = process_and_store_data(client_id, new_changed_content,  llm_cred, vectordb_cred)
            print("Stored in Milvus")
            if index == list_length - 1:
                update_web_storing(registrydb_params,client_id)       
            # return_text_content.append(text_data)
            # return_df.append(df.to_dict(orient='records'))



        return jsonify({'status': 'success', 'message': 'URLs uploaded and processed successfully'})


@app.route('/upload_url', methods=['POST'])
@cross_origin()
def upload_url():
    data = request.json
    client_id = data.get('client_id')
    urls = data.get('urls', [])
    max_depth = data.get('max_depth')
    frequency = data.get('frequency', 'none')  # Default to none
    end_time_str = data.get('end_time') 

    end_time = datetime.fromisoformat(end_time_str) if end_time_str else None

    # If frequency is set to "none", execute process_urls only once
    if frequency == 'none':
        process_urls(client_id, urls, max_depth)
        return jsonify({'status': 'success', 'message': 'URLs uploaded and processed successfully'})

    # Otherwise, schedule the process_urls function according to the specified frequency
    if frequency == 'minute':
        scheduler.add_job(process_urls, 'interval', minutes=2, max_instances=5, args=[client_id, urls, max_depth], end_date=end_time)
        print(f"Scraping will stop at: {end_time}")
    elif frequency == 'hour':
        scheduler.add_job(process_urls, 'interval', hours=1, max_instances=5, args=[client_id, urls, max_depth], end_date=end_time)
        print(f"Scraping will stop at: {end_time}")
    elif frequency == 'second':
        scheduler.add_job(process_urls, 'interval', seconds=5, max_instances=5, args=[client_id, urls, max_depth], end_date=end_time)
        print(f"Scraping will stop at: {end_time}")
    elif frequency == 'day':
        scheduler.add_job(process_urls, 'interval', days=1, max_instances=5, args=[client_id, urls, max_depth], end_date=end_time)
        print(f"Scraping will stop at: {end_time}")
    else:
        return jsonify({'status': 'error', 'message': 'Invalid frequency'})

    return jsonify({'status': 'success', 'message': f'URLs scheduled for processing, Scraping started for frequency every {frequency}'})






@app.route('/stop_scheduler', methods=['POST'])
@cross_origin()
def stop_scheduler():
    try:
        scheduler.pause()
        return jsonify({'status': 'success', 'message': 'Scheduler stopped successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/start_scheduler', methods=['POST'])
@cross_origin()
def start_scheduler():
    try:
        scheduler.resume()
        return jsonify({'status': 'success', 'message': 'Scheduler started successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})






# endpoint to handle audio files
@app.route('/upload_audio', methods=['POST'])
@cross_origin()
def upload_audio():
    # client_name = request.form.get('client_name')
    # audio_file = request.files['audio_file']

    # save_audio(client_name, audio_file)
    print("Audio Uploaded")

    return jsonify({'status': 'success', 'message': 'Audio uploaded successfully'})



# endpoint to handle image files
@app.route('/upload_image', methods=['POST'])
@cross_origin()
def upload_image():
    client_name = request.form.get('client_name')
    image_file = request.files['image_file']

    save_image(client_name, image_file)

    return 'Image file uploaded successfully'




# endpoint to handle document files
@app.route('/upload_file', methods=['POST'])
@cross_origin()
def upload_file():

    client_id = request.form.get('client_id')
    document_files = request.files.getlist('document_file')


    result_from_db = fetch_data_from_db(registrydb_params,client_id)
    llm_cred = {
        "api_base":result_from_db['api_base'],
        "api_key":result_from_db['api_key'],
        "api_type":result_from_db['api_type'],
        "api_version":result_from_db['api_version'],
        "embed_model":result_from_db['embed_model'],
        "embed_dim":result_from_db['embed_dim'],
        "completion_model":result_from_db['completion_model']
        }
    vectordb_cred = {
        "host_ip":result_from_db['vectordb_host'],
        "host_port":result_from_db['vectordb_port']}

    # client_cred = request.form.get("client_cred")
    # # client_cred=ast.literal_eval(client_cred)
    # client_cred = json.loads(client_cred)
    # llm_cred = request.form.get('llm_cred')
    # # llm_cred=ast.literal_eval(llm_cred)
    # llm_cred=json.loads(llm_cred)
    # vectordb_cred = request.form.get("vectordb_cred")  
    # vectordb_cred=json.loads(vectordb_cred)
    # vectordb_cred=ast.literal_eval(vectordb_cred)


    # requestData = request.json
    # client_cred = requestData.get("client_cred")
    # llm_cred = requestData.get('llm_cred')
    # vectordb_cred = requestData.get("vectordb_cred")   



    # print("scrapped_pdf")
    return_text_content = []
    return_df = []
    list_length = len(document_files)

    for index,file in enumerate(document_files):
        add_docu_name(registrydb_params, client_id,file.filename)
        text_content = read_file(file)
        if index == list_length - 1:
            update_docu_srcapping(registrydb_params,client_id)
        save_document(client_id, file)
        df = process_and_dump_openai(client_id, text_content, chunk_max_token, llm_cred, vectordb_cred)
        if index == list_length - 1:
            update_docu_storing(registrydb_params,client_id)       
        return_text_content.append(text_content)
        return_df.append(df.to_dict(orient='records'))

        # print(result_df)

   
    # print(text_content)

    return jsonify({'status': 'success', 'message': 'Data saved successfully', 'milvus_data': return_df ,  'text_content': return_text_content})



@app.route('/ask', methods=['POST'])
@cross_origin()
def ask():
         
    question = request.args.get("qstn")
    language = request.args.get("lang")
    print(question)
    print(language)
    requestData = request.json
    # chatHistory = r  equestData.get('chatHistory')
    # client_cred = requestData.get("client_cred")
    # vectordb_cred = requestData.get("vectordb_cred")
    # llm_cred = requestData.get("llm_cred")
    # client_id = client_cred["client_name"]+"_"+client_cred["project_name"]

    client_id = requestData.get('client_id')
    print(client_id)
    result_from_db = fetch_data_from_db(registrydb_params,client_id)
    llm_cred = {
        "api_base":result_from_db['api_base'],
        "api_key":result_from_db['api_key'],
        "api_type":result_from_db['api_type'],
        "api_version":result_from_db['api_version'],
        "embed_model":result_from_db['embed_model'],
        "embed_dim":result_from_db['embed_dim'],
        "completion_model":result_from_db['completion_model']
        }
    # vectordb_cred = {
    #     "host_ip":result_from_db['vectordb_host'],
    #     "host_port":result_from_db['vectordb_port']}

    print("rdb okay")
    MILVUS_HOST = result_from_db['vectordb_host']
    MILVUS_PORT = result_from_db['vectordb_port']

    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
    collection = Collection(client_id)
    # collection = Collection("demo_demo_d3f28c3b_f0e0_48b3_a2a4_a5e67fd8da78")
    collection.load()
    ansr = final_search(llm_cred, collection_in=collection, question_in=question, language_in=language) #, source_in = source, destination_in = destination , , chatHistory=chatHistory, session_id_in = session_id   #, sentiment, context

    return jsonify({
    "answer": ansr,
    "status": 200
})



# driver function
if __name__ == '__main__':
    CORS(app, support_credentials=True)
    app.run(host='0.0.0.0',port=8000)



##################################################################

# # Route to handle URL uploads
# @app.route('/upload_url', methods=['POST'])
# def upload_url():
#     client_name = request.form.get('client_name')
#     url = request.form.get('url')

#     save_url(client_name, url)

#     return 'URL uploaded successfully'

# Route to handle audio file uploads



# # Route to handle document file uploads (PDF, DOCX, etc.)
# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     client_name = request.form.get('client_name')
#     document_file = request.files['document_file']

#     # Save the document file
#     save_document(client_name, document_file)

#     return 'Document file uploaded successfully'






# def save_document(client_name, document_file):
#     # Extract text from the document
#     text_content = extract_text_from_document(document_file)

#     # Save the extracted text into a TXT file in the 'url' folder
#     save_text_to_file(client_name, 'url', 'extracted_text', text_content)




# @app.route('/fetch_data', methods=['GET'])
# def fetch_data():
#     result = fetch_all_projects(db_params)

#     if result:
#         client_data, url_data = result

#         response_data = {
#             'client_data': client_data,
#             'url_data': url_data
#         }

#         return jsonify(response_data)
#     else:
#         return jsonify({'error': 'Failed to fetch data from the database'}), 500





# def extract_text_from_document(document_file):

#     return "Extracted text from the document"





# def extract_text_from_document(document_file):
#     # Implement text extraction logic for PDF, DOCX, etc.
#     # Use the functions from file_functions.py as needed
#     return "Extracted text from the document"



# PostgreSQL database connection parameters
# db_params = {
#     'host': 'genaidbserver.postgres.database.azure.com',
#     'port': 5432,
#     'user': 'ravinder',
#     'password': 'Admin@345',
#     'dbname': 'gen_ai_db'
# }
    


# Milvus DB server configurations
# MILVUS_HOST = '20.244.48.175'  # Milvus server URI #vector DB host server IP for Dev
# MILVUS_PORT = '19530' #Milvus port number
    




# openai.api_base = "https://sravanakumar13sathish.openai.azure.com/"  
# openai.api_base = "https://soumenopenai.openai.azure.com" 
# openai.api_key = "xxxxxxxxx"
# openai.api_type = 'azure'
# openai.api_version = "2023-03-15-preview"
# EMBEDDING_MODEL="text-embedding-ada-002"
# CHAT_COMPLETION_MODEL = 'gpt-35-turbo-16k-soumen'
