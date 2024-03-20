#combined text where ind[0] have all info about page 1
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os
import re
import datetime

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

global link_data, successful_links, unsuccessful_links
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
        print(f"Skipping {url} - Already visited")
        return [], links_final, json_data  

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
        print(f"Error scraping {url}: {e}")
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



if __name__ == "__main__":
    start_url = "https://www.itchotels.com/"
    depth = 2
    client_name = "client_01"

    print("Scraping website...")
  
    extracted_text_list, links_dict, json_data = scrape_website2(start_url, depth, client_name = client_name)  

    directory = "extracted_data_json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file_path = "extracted_data_json/textual_data_{timestamp}.json"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = output_file_path.format(timestamp=timestamp)

    with open(output_file_path, "w+") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("Scraping complete and  saved Json!")


    # previous_json_path = "scraped_data.json"
    # current_json_path = "scraped_data.json"
    # changed_urls = compare_jsons(previous_json_path, current_json_path)
    # print("No of changed urls:", len(changed_urls))
