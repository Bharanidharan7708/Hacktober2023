import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
import datetime
import time
import pandas as pd
from io import BytesIO
import csv
import PyPDF2
from docx import Document
 
def read_pdf(file_buffer):
    # print("Hello 2")
    pdf_reader = PyPDF2.PdfReader(file_buffer)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
       
    return text
 
 
def read_docx(file_buffer):
    doc = Document(file_buffer)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
 
 
def read_excel(file_buffer):
    df = pd.read_excel(file_buffer, sheet_name=None)
    text = ''
    for sheet_name, sheet_data in df.items():
        text += f"\nSheet: {sheet_name}\n"
        text += sheet_data.to_string(index=False) + '\n'
    return text
 
 
def read_csv(file_buffer):
    text = file_buffer.getvalue().decode('utf-8')
    reader = csv.reader(text.splitlines())
    result = ''
    for row in reader:
        result += ', '.join(row) + '\n'
    return result
 
 
def read_txt(file_buffer):
    text = file_buffer.getvalue().decode('utf-8')
    return text
 
 
def extract_files(soup, base_url):
    # print('Hello')
    files = soup.find_all('a', href=True)
    file_urls = []
    for file in files:
        file_url = urljoin(base_url, file['href'])
        if file_url.endswith(('.pdf', '.csv', '.xlsx', '.xls', '.doc', '.docx', '.txt')):  # Add more extensions if needed
            file_urls.append(file_url)
    file_texts = {}
    for url in file_urls:
        file_texts[url] = read_file(url)  
    return file_texts
 
 
def read_file(url):
    # print("Hello 1")
    response = requests.get(url)
    file_buffer = BytesIO(response.content)
    file_extension = url.rsplit('.', 1)[1].lower()
 
    if file_extension == 'pdf':
        return read_pdf(file_buffer)
    elif file_extension in ['doc', 'docx']:
        return read_docx(file_buffer)
    elif file_extension in ['xls', 'xlsx']:
        return read_excel(file_buffer)
    elif file_extension == 'csv':
        return read_csv(file_buffer)
    elif file_extension == 'txt':
        return read_txt(file_buffer)
    else:
        return "Unsupported file format."
 
def extract_title(soup):
    title_tag = soup.title
    return title_tag.text.strip() if title_tag else None
 
def extract_paragraphs(soup):
    paragraphs = soup.select('p')
    return [p.text.strip() for p in paragraphs]
 
def extract_headings(soup, tag):
    headings = soup.select(tag)
    return [heading.text.strip() for heading in headings]
 
def extract_lists(soup):
    lists_text = soup.select('li')
    return [li.text.strip() for li in lists_text]
 
def extract_images(soup):
    images = soup.select('img')
    return [img['src'] for img in images]
 
def clean_text(raw_text):
    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    cleaned_text = re.sub(r'\n', '', cleaned_text)
    cleaned_text = re.sub(r'\r', '', cleaned_text)
    cleaned_text = re.sub(r'\xa0', '', cleaned_text)
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  
    cleaned_text = cleaned_text.strip()
    return cleaned_text
 
 
def scrape_website(url, max_depth, client_name):
    # print("Scraping started for client_id:", client_name)
    # print("Scraping URL:", url)
    text, links_dict, json_data = scrape_website2(url, max_depth, client_name)
 
    last_run_file = get_latest_json_file("extracted_data_json/")
    save_data(json_data)
    time.sleep(2)  # Wait for 2 seconds to ensure the file is saved
    current_run_file = get_latest_json_file("extracted_data_json/")
 
    new_changed_content = {}
    if last_run_file and current_run_file:
        new_changed_content = compare_jsons(last_run_file, current_run_file)
        print("Number of contents changed:", len(new_changed_content))
    else:
        print("Unable to compare. One or both JSON files not found.")
 
    # print("Scrape done!")
    return text, links_dict, new_changed_content
 
 
def scrape_website2(url, max_depth, client_name, current_depth=1, visited=None, link_data=None, successful_links=None, unsuccessful_links=None, json_data=None):
    combined_text = []
    if visited is None:
        visited = set()
    if link_data is None:
        link_data = {"url": [], "status_code": [], "text": [], "title": [], "paragraphs": [],
                     "h1_headings": [], "h2_headings": [], "h3_headings": [],
                     "h4_headings": [], "lists": [], "images": [], "metadata": []}
    if successful_links is None:
        successful_links = {"url": [], "status_code": []}
    if unsuccessful_links is None:
        unsuccessful_links = {"url": [], "status_code": []}
    if json_data is None:
        json_data = {"url":[], "content":[]}
 
    links_final = {}  
 
    if current_depth > max_depth:
        return [], links_final, json_data  
 
    if url in visited:
        # print(f"Skipping {url} - Already visited")
        return [], links_final, json_data  
 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)
 
            # print(f"Scraping {url}")
            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            page_info = ""
            page_info += " ".join(title for title in extract_title(soup) if title) + "\n"
            page_info += " ".join(paragraph for paragraph in extract_paragraphs(soup) if paragraph) + "\n"
            page_info += " ".join(heading for heading in extract_headings(soup, 'h1') if heading) + "\n"
            page_info += " ".join(heading for heading in extract_headings(soup, 'h2') if heading) + "\n"
            page_info += " ".join(heading for heading in extract_headings(soup, 'h3') if heading) + "\n"
            page_info += " ".join(heading for heading in extract_headings(soup, 'h4') if heading) + "\n"
            page_info += " ".join(list_item for list_item in extract_lists(soup) if list_item) + "\n"
            combined_text.append(page_info)
            json_data['url'].append(url)
            json_data['content'].append(page_info)
 
 
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                page_info, _, _ = scrape_website2(next_url, max_depth, client_name, current_depth + 1, visited, link_data, successful_links, unsuccessful_links, json_data)
                combined_text.extend(page_info)
 
            successful_links["url"].append(url)
            successful_links["status_code"].append(response.status_code)
        else:
            unsuccessful_links["url"].append(url)
            unsuccessful_links["status_code"].append(response.status_code)
            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            link_data["text"].append(" ")
            link_data["title"].append(" ")
            link_data["paragraphs"].append(" ")
            link_data["h1_headings"].append(" ")
            link_data["h2_headings"].append(" ")
            link_data["h3_headings"].append(" ")
            link_data["h4_headings"].append(" ")
            link_data["lists"].append(" ")
            link_data["images"].append(" ")
    except Exception as e:
        # print(f"Error scraping {url}: {e}")
        unsuccessful_links["url"].append(url)
        unsuccessful_links["status_code"].append("Error")
 
    links_final = {"link_success": successful_links['url'], "link_failure": unsuccessful_links['url']}
    final_text = []
 
    for i in range(len(combined_text)):
        final_text.append(combined_text[i] + " Source Link: " + links_final['link_success'][i])
    json_list = []
    for url, content in zip(json_data['url'], json_data['content']):
        json_list.append({"url": url, "content": content})
    return final_text, links_final, json_list
 
def save_data(json_data):
    directory = "extracted_data_json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file_path = "extracted_data_json/textual_data_{timestamp}.json"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = output_file_path.format(timestamp=timestamp)
 
    with open(output_file_path, "w+") as json_file:
        json.dump(json_data, json_file, indent=4)
 
 
def compare_jsons(previous_json_path, current_json_path):
    with open(previous_json_path, "r") as f:
        previous_json = json.load(f)
    with open(current_json_path, "r") as f:
        current_json = json.load(f)
 
    if isinstance(previous_json, list) and isinstance(current_json, list):
        previous_urls = {entry["url"]: entry["content"] for entry in previous_json}
        current_urls = {entry["url"]: entry["content"] for entry in current_json}
    else:
        previous_urls = previous_json
        current_urls = current_json
    if previous_urls == current_urls:
        return {}  # No changes
 
    changed_urls = {}
 
    for url, previous_content in previous_urls.items():
        if url in current_urls:
            current_content = current_urls[url]
            if previous_content.strip() != current_content.strip():
                changed_urls[url] = current_content
        else:
            changed_urls[url] = "URL no longer exists"
 
    new_urls = {url: content for url, content in current_urls.items() if url not in previous_urls}
    changed_urls.update(new_urls)
 
    return changed_urls
 
 
def get_latest_json_file(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    files = os.listdir(directory)
    files = [file for file in files if file.endswith(".json")]
    if not files:
        return None  # No JSON files found
    latest_file = max(files)
    return os.path.join(directory, latest_file)
 
def scrape_website_files(url, max_depth, client_name, current_depth=1, visited=None, file_text=None):
    if visited is None:
        visited = set()
    if file_text is None:
        file_text = {"url": [], "data": []}
 
    if current_depth > max_depth:
        return file_text
 
    if url in visited:
        return file_text
 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)
 
            # Extract files and their text
            file_texts = extract_files(soup, url)
 
            # Append file texts to the file_text dictionary
            for file_url, file_text_value in file_texts.items():
                # Clean the extracted text
                cleaned_text = clean_text(file_text_value)
                # Append cleaned text to the file_text dictionary
                file_text["url"].append(file_url)
                file_text["data"].append(cleaned_text)
 
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                file_text = scrape_website_files(next_url, max_depth, client_name, current_depth + 1, visited, file_text)
 
        else:
            print(f"Unsuccessful request for {url}. Status code: {response.status_code}")
 
    except Exception as e:
        print(f"Error scraping {url}: {e}")    
        save_data_file(file_text)
    return file_text
 
 
def save_data_file(file_text):
    directory = "extracted_file_data_json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file_path = "extracted_file_data_json/textual_data_{timestamp}.json"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = output_file_path.format(timestamp=timestamp)
 
    with open(output_file_path, "w+") as json_file:
        json.dump(file_text, json_file, indent=4)
 
if __name__ == "__main__":
    start_url = "https://milvus.io/blog/what-milvus-version-to-start-with.md"
    depth = 2
    client_name = "client_01"
 
    scrape_website(start_url, depth, client_name)
    scrape_website_files(start_url, depth, client_name)
