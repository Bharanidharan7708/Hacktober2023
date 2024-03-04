import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os

def scrape_website(url, max_depth, client_name, current_depth=1, visited=None, link_data=None, successful_links=None, unsuccessful_links=None):
    if visited is None:
        visited = set()
    if link_data is None:
        link_data = {"url": [], "status_code": [], "text": []}
    if successful_links is None:
        successful_links = {"url": [], "status_code": []}
    if unsuccessful_links is None:
        unsuccessful_links = {"url": [], "status_code": []}

    if current_depth > max_depth:
        return

    if url in visited:
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)

            print(f"Scraping {url}")
            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            link_data["text"].append(soup.get_text())

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
            link_data["text"].append(None)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        unsuccessful_links["url"].append(url)
        unsuccessful_links["status_code"].append("Error")
        link_data["url"].append(url)
        link_data["status_code"].append("Error")
        link_data["text"].append(None)

    client_folder = os.path.join(os.getcwd(), client_name)
    os.makedirs(client_folder, exist_ok=True)
    link_df = pd.DataFrame(link_data)
    successful_links_df = pd.DataFrame(successful_links)
    unsuccessful_links_df = pd.DataFrame(unsuccessful_links)

    link_df.to_csv(os.path.join(client_folder, "link_data.csv"), index=False)
    successful_links_df.to_csv(os.path.join(client_folder, "successful_links.csv"), index=False)
    unsuccessful_links_df.to_csv(os.path.join(client_folder, "unsuccessful_links.csv"), index=False)

if __name__ == "__main__":
    start_url = "https://stackoverflow.com/questions/9265172/scrape-an-entire-website"
    depth = 2
    client_name = "client_01"

    print("Scraping website...")
    link_data = {"url": [], "status_code": [], "text": []}
    successful_links = {"url": [], "status_code": []}
    unsuccessful_links = {"url": [], "status_code": []}
    scrape_website(start_url, depth, client_name, link_data=link_data, successful_links=successful_links, unsuccessful_links=unsuccessful_links)

    print("Scraping complete!")
