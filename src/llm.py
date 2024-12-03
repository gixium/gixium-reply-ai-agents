import re
import openai
KEY = "KEY_HERE"
PROMPT = """
### SYSTEM PROMPT
You are a skilled expert web scraper. 
You are able find a lot of hidden information, hidden but reliable.
You can't deliver unreliable information.
Don't use knowledge not in the page to answer the question.

You are given the content of a webpage.
Stick your research field to the links you find in the page.
You are able to navigate all the pertinent links in the page. 
If a link to explore further is available, show it.

If you can't find the answer in the current page, visit another one.
To visit another page use 
```website 
link 
```
Visit the specialized pages if it is useful for the query.
### USER SETTINGS
You are navigating the {uni_site} website and its subpages.
Structure your answer by giving a short answer right away, then optionally give a detailed explanation with correlated information (if there is any).

### USER PROMPT
{user_prompt}
"""

def start_interaction(message):
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": message},
    ]
    return generate(message)

def analyze_website(request, page_content, page_url, history=[]):
    messages = [
        {"role": "system", "content": PROMPT.format(uni_site=page_url, user_prompt=request)},
    ]
    messages += history
    messages.append({"role": "user", "content": page_content})
    return generate(messages)
def ask(question, history):
    messages = [
        {"role": "system", "content": PROMPT},
    ]
    messages += history
    messages.append({"role": "user", "content": question})
    return generate(messages)

def generate(messages):
    client = openai.Client(api_key=KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
    final_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            final_response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)  # Print each chunk in real-time

    print()  # For a new line after the response is complete
    return final_response

def extract_code_blocks_with_language(text):
    # Regular expression pattern to match code blocks with optional language identifier
    pattern = r'```(.*?)(?:\n(.*?))```'
    
    # Use re.DOTALL to make the dot (.) match newline characters as well
    code_blocks_with_language = re.findall(pattern, text, re.DOTALL)
    
    # Process the matches to separate language and code
    result = []
    for match in code_blocks_with_language:
        language = match[0].strip() if match[0] else None
        code = match[1].strip() if match[1] else None
        result.append((language, code))
    
    return result
