from bs4 import BeautifulSoup
from markdownify import markdownify as md
def clean_html_to_markdown(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove images
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remove style and script tags
    for tag in soup(['style', 'script']):
        tag.decompose()
    
    # Remove all tags except links, paragraphs, lists, bold, italic
    for tag in soup.find_all(True):
        if tag.name not in ['a', 'p', 'ul', 'ol', 'li', 'b', 'strong', 'i', 'em']:
            tag.unwrap()
    
    # Convert the cleaned HTML to Markdown
    markdown_content = md(str(soup))
    
    # Extract links and format them as a list
    links = []
    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.get_text(strip=True)
        link_url = a_tag['href']
        links.append(f"- [{link_text}]({link_url})")
    
    # Join the links into a single string
    links_list = "\n".join(links)
    
    # Combine the Markdown content and the links list
    final_content = f"{markdown_content}\n\n## Links\n{links_list}"
    
    return final_content
