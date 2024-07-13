import markdown
from gtts import gTTS
import os

def markdown_to_speech(md_text, output_filename):
    # Convert Markdown text to HTML
    html = markdown.markdown(md_text)
    
    # Process HTML to create a speech-friendly version
    # This can be as simple or as complex as you need
    # For now, we'll just replace some HTML tags with readable text
    speech_text = html.replace('<h1>', 'Header one: ').replace('</h1>', '. ')
    speech_text = speech_text.replace('<h2>', 'Header two: ').replace('</h2>', '. ')
    speech_text = speech_text.replace('<ul>', '').replace('</ul>', '')
    speech_text = speech_text.replace('<li>', 'List item: ').replace('</li>', '. ')
    speech_text = speech_text.replace('<p>', '').replace('</p>', '. ')

    # Convert processed text to speech
    tts = gTTS(speech_text, lang='en')
    tts.save(output_filename)

# Example Markdown text
md_text = """
# Heading One

Welcome to my world.

## Heading Two

Regular text.

- List item 1
- List item 2

"""

# Convert Markdown to speech
markdown_to_speech(md_text, "output.mp3")

# Play the MP3 file (assuming pygame is still being used)
# play_mp3("output.mp3")
