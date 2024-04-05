import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
import datetime
import time 
import json

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

def extract_elements(soup, tags):
    elements = []
    for tag in tags:
        extracted = soup.find_all(tag)
        elements.extend([elem.text.strip() for elem in extracted])
    return elements


def scrape_website2(url, max_depth, current_depth=1, visited=None, link_data=None, successful_links=None, unsuccessful_links=None, json_data=None):
    combined_text = []
    
    if visited is None:
        visited = set()
    if link_data is None:
        link_data = {"url": [], "status_code": [], "text": [], "title": [], "paragraphs": [],
                     "headings": [], "lists": [], "images": [], "metadata": []}
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
        return [], links_final, json_data  

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)

            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            page_info = ""

            title = extract_title(soup)
            if title:
                page_info += title + "\n"

            paragraphs = extract_elements(soup, ['p', 'div', 'span'])
            page_info += " ".join(paragraph for paragraph in paragraphs if paragraph) + "\n"

            headings = extract_elements(soup, ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            page_info += " ".join(heading for heading in headings if heading) + "\n"

            lists = extract_elements(soup, ['ul', 'ol'])
            page_info += " ".join(list_item for list_item in lists if list_item) + "\n"

            images = extract_images(soup)
            page_info += " ".join(image for image in images if image) + "\n"

            combined_text.append(page_info)
            json_data['url'].append(url)
            json_data['content'].append(page_info)

            # Extracting links for further scraping
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                page_info, _, _ = scrape_website2(next_url, max_depth, current_depth + 1, visited, link_data, successful_links, unsuccessful_links, json_data)
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
            link_data["headings"].append(" ")
            link_data["lists"].append(" ")
            link_data["images"].append(" ")
    except Exception as _:
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


def scrape_website(url, max_depth):
    print("Scraping URL:", url)
    text, links_dict, json_data_web = scrape_website2(url, max_depth)
    return text, links_dict

def save_to_text_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for page_content in data:
            file.write(page_content)
            file.write('\n\n')  

    print(f"Data saved to {filename}")


start_url = "https://www.icicibank.com/online-safe-banking/report-fraud#:~:text=To%20report%20Internet%20Banking%2C%20Credit,Customer%20Care%20on%201800%202662."
depth = 2
client_name = "ClientName"
current_dir = os.getcwd()
client_path = os.path.join(current_dir, "uploads", client_name)

scrapped_text, link_status_urls = scrape_website(start_url, depth)
filename = 'C:/Users/Bharani/Desktop/Genai/extracted_data.txt'
save_to_text_file(scrapped_text, filename)
print(link_status_urls)
