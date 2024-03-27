[3:06 PM] Dipyaman De (IN)
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os
from io import BytesIO
import datetime
import PyPDF2
from docx import Document
import csv
 
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
 
def read_pdf(file_buffer):
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
    files = soup.find_all('a', href=True)
    file_urls = []
    for file in files:
        file_url = urljoin(base_url, file['href'])
        if file_url.endswith(('.pdf', '.csv', '.xlsx', '.xls', '.doc', '.docx', '.txt')):
            file_urls.append(file_url)
    file_texts = {}
    for url in file_urls:
        file_texts[url] = read_file(url)
    return file_texts
 
def read_file(url):
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
 
global link_data, successful_links, unsuccessful_links
def scrape_website2(url, max_depth, client_name, current_depth=1, visited=None, link_data=None, successful_links=None, unsuccessful_links=None, json_data=None, file_text=None):
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
    if file_text is None:
        file_text = {"url": [], "data": []}
    if json_data is None:
        json_data = {"url": [], "content": []}
 
    links_final = {}
 
    if current_depth > max_depth:
        return combined_text, links_final, json_data, file_text
 
    if url in visited:
        print(f"Skipping {url} - Already visited")
        return combined_text, links_final, json_data, file_text
 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)
 
            print(f"Scraping {url}")
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
 
            # Extract files and their text
            file_texts = extract_files(soup, url)
            # Append file texts to the file_text dictionary
            for file_url, file_text_value in file_texts.items():
                file_text["url"].append(file_url)
                file_text["data"].append(file_text_value)
 
            # Append file texts to the combined_text list
            for file_text_value in file_texts.values():
                combined_text.append(file_text_value)
 
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                page_info, _, _, _ = scrape_website2(next_url, max_depth, client_name, current_depth + 1, visited, link_data, successful_links, unsuccessful_links, json_data, file_text)
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
        print(f"Error scraping {url}: {e}")
        unsuccessful_links["url"].append(url)
        unsuccessful_links["status_code"].append("Error")
 
    links_final = {"link_success": successful_links['url'], "link_failure": unsuccessful_links['url']}
    final_text = []
 
    min_len = min(len(combined_text), len(links_final['link_success']))
    for i in range(min_len):
        final_text.append(combined_text[i] + " Source Link: " + links_final['link_success'][i])
 
    json_list = []
    for url, content in zip(json_data['url'], json_data['content']):
        json_list.append({"url": url, "content": content})
 
    return final_text, links_final, json_list, file_text
 
 
def save_json_data(json_data, output_file_path):
    with open(output_file_path, "w+") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("JSON data saved successfully!")
 
 
 
if __name__ == "__main__":
    #start_url = "https://www.itchotels.com/"
    start_url="https://milvus.io/blog/what-milvus-version-to-start-with.md"
    depth = 2
    client_name = "client_01"
 
    print("Scraping website...")
 
    extracted_text_list, links_dict, json_data, file_text = scrape_website2(start_url, depth, client_name=client_name)  
 
    # Save textual data to JSON
    directory = "extracted_data_json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file_path = f"extracted_data_json/textual_data_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
 
    save_json_data(json_data, output_file_path)
    print("Scraping complete and saved textual data to JSON!")
     
    # Save file text data to JSON
    directory = "extracted_file_data_json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file_path1 = f"extracted_file_data_json/file_text_data_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
 
    save_json_data(file_text, output_file_path1)
    print("Scraping complete and saved file text data to JSON!")
    # Example of comparing two JSON files
    # previous_json_path = "previous_data.json"
    # current_json_path = "current_data.json"
    # changed_urls = compare_jsons(previous_json_path, current_json_path)
    # print("Changed URLs:", changed_urls)
 
 
