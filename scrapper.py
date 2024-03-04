
    for title in link_data['title']:
        if title:
            combined_text.extend(title)

    for paragraph in link_data['paragraphs']:
        if paragraph:
            combined_text.extend(paragraph)

    combined_text = ''.join(combined_text)


    links_final = {"link_success": successful_links['url'], "link_failure": unsuccessful_links['url']} 
