import wikipediaapi
from gtts import gTTS

Agent = 'User-Agent: MyBot/0.0 (https://mysite); admin@mysite) generic-library/0.0'
Words = 1000

# Function to get wikipedia page content
def get_wikipedia_content(page_title):
    wiki_wiki = wikipediaapi.Wikipedia(Agent)
    page = wiki_wiki.page(page_title)
    return page.text

# Function to get wikipedia random page content

def get_random_wikipedia_article(lang='en'):
    wiki_wiki = wikipediaapi.Wikipedia(Agent)
    random_page = wiki_wiki.page(wiki_wiki.randompages(1)[0].title)
    return random_page.text

# Specify the Wikipedia page and section you want to convert
page_title = 'Chicken'

# Fetch the content
# content = get_wikipedia_content(page_title)
content = get_random_wikipedia_article()

# Truncate to the first 500 characters for brevity (you can adjust this)
content_to_read = content[:Words]

print("Title:", page_title.title)
print("Summary:", page_title.summary[0:Words])  # Printing the first N characters of the summary

# Convert text to speech
tts = gTTS(text=content_to_read, lang='en')
tts.save(page_title + ".mp3")

print(f"Audio file created for page: {page_title}")

