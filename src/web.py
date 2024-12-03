from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrape import clean_html_to_markdown
from llm import ask, analyze_website, extract_code_blocks_with_language
# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line if you want to run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver
service = Service()  # Update this path to where your chromedriver is located
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_html_from_url(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    return driver.page_source 

user_input = input("[*] User Message: ")
base_url = "https://polimi.it"
current_website = "https://polimi.it"
conversation_history = []
link = False
old_link = ""
while user_input != "exit":
    if not link:
        conversation_history.append({"role": "user", "content": user_input})
    if current_website != old_link:
        old_link = current_website
        print("new website: " + current_website)
        website_html = get_html_from_url(current_website)
        cleaned_html = clean_html_to_markdown(website_html)
        print("\n\n[*] Assistant: ")
        bot_output = analyze_website(user_input, cleaned_html, current_website, conversation_history)
    else:
        print("\n[*] Assistant: ")
        bot_output = ask(user_input,conversation_history)
    conversation_history.append({"role": "assistant", "content": bot_output})
    actions = extract_code_blocks_with_language(bot_output)
    link = False
    for action in actions:
        if action[0] == "website" and action[1] != old_link and (base_url + action[1]) != old_link:
            current_website = action[1]
            if not current_website.startswith("https://"):
                current_website = base_url + current_website
            link = True
            break
    if not link: 
        print("\n\n\nFinal Answer: " + bot_output)
        user_input = input("Message: ")

print("Goodbye!")
driver.quit()
