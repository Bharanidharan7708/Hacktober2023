# Import necessary modules and functions
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

# Define the function extract_title, extract_elements, and extract_images if they are not already defined

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

def scrape_website2(url, max_depth):
    # Initialize necessary variables
    visited = set()
    link_data = {"url": [], "status_code": [], "text": [], "title": [], "paragraphs": [],
                 "headings": [], "lists": [], "images": [], "metadata": []}
    successful_links = {"url": [], "status_code": []}
    unsuccessful_links = {"url": [], "status_code": []}
    json_data = {"url": [], "content": []}
    
    # Call the main scraping function
    final_text, links_final, json_list = scrape_website2_recursive(url, max_depth, 1, visited, link_data, successful_links, unsuccessful_links, json_data)

    # Return the extracted data
    return final_text, links_final, json_list

def scrape_website2_recursive(url, max_depth, current_depth, visited, link_data, successful_links, unsuccessful_links, json_data):
    combined_text = []
    
    # Check if maximum depth is reached
    if current_depth > max_depth:
        return [], {"link_success": [], "link_failure": []}, {"url": [], "content": []}
    
    # Check if URL is already visited
    if url in visited:
        return [], {"link_success": [], "link_failure": []}, {"url": [], "content": []}
    
    try:
        # Send HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            visited.add(url)

            # Extracting useful information
            link_data["url"].append(url)
            link_data["status_code"].append(response.status_code)
            page_info = ""

            # Extracting title
            title = extract_title(soup)
            if title:
                page_info += title + "\n"

            # Extracting paragraphs, headings, lists, and images
            tags_to_extract = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'img']
            elements = extract_elements(soup, tags_to_extract)
            for element in elements:
                page_info += element + "\n"

            # Append the page info to the combined text
            combined_text.append(page_info)

            # Extracting links for further scraping
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                # Recursively call the function for each link
                page_info, _, _ = scrape_website2_recursive(next_url, max_depth, current_depth + 1, visited, link_data, successful_links, unsuccessful_links, json_data)
                combined_text.extend(page_info)

            # Record successful link
            successful_links["url"].append(url)
            successful_links["status_code"].append(response.status_code)
        else:
            # Record unsuccessful link
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
    except Exception as e:
        # Record error for unsuccessful link
        unsuccessful_links["url"].append(url)
        unsuccessful_links["status_code"].append("Error")

    # Construct final links dictionary
    links_final = {"link_success": successful_links['url'], "link_failure": unsuccessful_links['url']}

    # Combine page info with source links
    final_text = [info + " Source Link: " + links_final['link_success'][i] for i, info in enumerate(combined_text)]
    
    # Prepare JSON data
    json_list = [{"url": url, "content": content} for url, content in zip(json_data['url'], json_data['content'])]

    return final_text, links_final

def save_to_text_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for page_content in data:
            file.write(page_content)
            file.write('\n\n')  # Add a new line between each page's content

# Example usage:
    print(f"Data saved to {filename}")


# Now you can call the function scrape_website2 with the URL and depth parameters
url = "https://www.icicibank.com/online-safe-banking/report-fraud#:~:text=To%20report%20Internet%20Banking%2C%20Credit,Customer%20Care%20on%201800%202662."
depth = 2
final_text, links_final  = scrape_website2(url, depth)
filename = 'D:/Work/ConvoCraft/src/extracted_data.txt'
save_to_text_file(final_text, filename)
print("Done...")
