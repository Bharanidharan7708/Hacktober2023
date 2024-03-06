#combined text where ind[0] have all info about page 1

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os
import re

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

combined_text = []  #for final extracted_text_list

def scrape_website(url, max_depth, client_name, current_depth=1, visited=None, link_data=None, successful_links=None, unsuccessful_links=None):
    if visited is None:
        visited = set()
    if link_data is None:
        link_data = {"url": [], "status_code": [], "text": [], "title": [], "paragraphs": [],
                     "h1_headings": [], "h2_headings": [], "h3_headings": [],
                     "h4_headings": [], "lists": [], "images": []}
    if successful_links is None:
        successful_links = {"url": [], "status_code": []}
    if unsuccessful_links is None:
        unsuccessful_links = {"url": [], "status_code": []}

    links_final = {}  

    if current_depth > max_depth:
        return combined_text, links_final   

    if url in visited:
        return combined_text, links_final   

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)

            print(f"Scraping {url}")
            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            link_data["text"].append(soup.get_text())
            link_data["title"].append(extract_title(soup) if extract_title(soup) is not None else None)
            link_data["paragraphs"].append(extract_paragraphs(soup))
            link_data["h1_headings"].append(extract_headings(soup, 'h1'))
            link_data["h2_headings"].append(extract_headings(soup, 'h2'))
            link_data["h3_headings"].append(extract_headings(soup, 'h3'))
            link_data["h4_headings"].append(extract_headings(soup, 'h4'))
            link_data["lists"].append(extract_lists(soup))
            link_data["images"].append(extract_images(soup))

            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                scrape_website(next_url, max_depth, client_name, current_depth + 1, visited, link_data, successful_links, unsuccessful_links)
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
        link_data["url"].append(url)
        link_data["status_code"].append("Error")
        link_data["text"].append(" ")
        link_data["title"].append(" ")
        link_data["paragraphs"].append(" ")
        link_data["h1_headings"].append(" ")
        link_data["h2_headings"].append(" ")
        link_data["h3_headings"].append(" ")
        link_data["h4_headings"].append(" ")
        link_data["lists"].append(" ")
        link_data["images"].append(" ")

    client_folder = os.path.join(os.getcwd(), client_name)
    os.makedirs(client_folder, exist_ok=True)
    
    # Pading arrays to ensure consistent length - to avoid previous error 
    max_length = max(len(link_data[key]) for key in link_data)
    for key in link_data:
        link_data[key] += [None] * (max_length - len(link_data[key]))

    page_info = ""
    page_info += " ".join(title for title in link_data['title'] if title) + "\n"
    page_info += " ".join(paragraph for sublist in link_data['paragraphs'] for paragraph in sublist if paragraph) + "\n"
    page_info += " ".join(heading for sublist in link_data['h1_headings'] for heading in sublist if heading) + "\n"
    page_info += " ".join(heading for sublist in link_data['h2_headings'] for heading in sublist if heading) + "\n"
    page_info += " ".join(heading for sublist in link_data['h3_headings'] for heading in sublist if heading) + "\n"
    page_info += " ".join(heading for sublist in link_data['h4_headings'] for heading in sublist if heading) + "\n"
    page_info += " ".join(list_extracted for sublist in link_data['lists'] for list_extracted in sublist if list_extracted)

    combined_text.append(page_info)

    links_final = {"link_success": successful_links['url'], "link_failure": unsuccessful_links['url']}   

    link_df = pd.DataFrame(link_data)
    successful_links_df = pd.DataFrame(successful_links)
    unsuccessful_links_df = pd.DataFrame(unsuccessful_links)

    link_df.to_csv(os.path.join(client_folder, "link_data.csv"), index=False)
    successful_links_df.to_csv(os.path.join(client_folder, "successful_links.csv"), index=False)
    unsuccessful_links_df.to_csv(os.path.join(client_folder, "unsuccessful_links.csv"), index=False)

    return combined_text, links_final


if __name__ == "__main__":
    start_url = "https://itchotels.com"
    depth = 2
    client_name = "client_01"

    print("Scraping website...")
    link_data = {"url": [], "status_code": [], "text": [], "title": [], "paragraphs": [],
                 "h1_headings": [], "h2_headings": [], "h3_headings": [],
                 "h4_headings": [], "lists": [], "images": []}
    successful_links = {"url": [], "status_code": []}
    unsuccessful_links = {"url": [], "status_code": []}
    extracted_text_list, links_dict = scrape_website(start_url, depth, client_name, link_data=link_data, successful_links=successful_links, unsuccessful_links=unsuccessful_links)  # Corrected line
    text = [clean_text(text_list) for text_list in extracted_text_list]

    print("Scraping complete!")
