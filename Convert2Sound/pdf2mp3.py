# This code converts .pdf to .mp3
# importing the modules

import os
import re
import sys
import subprocess
import importlib.util
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment 
import PyPDF2
import pygame
import time

# path of the PDF file
 
# path = 'd:/Project/test.pdf'
path = 'test.pdf'

required_modules = ['pyttsx3', 'gtts', 'pydub', 'PyPDF2', 're', 'os', 'pygame']

# Define voices for pyttsx3
voices = {
    'UK': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0',
    'US': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
}

# Define language codes for gTTS
lang_codes = {
    'UK': 'en-uk',
    'US': 'en-us'
}

# User's choice for region
user_choice = 'UK'  # or 'US'

def check_dependencies(modules):
    missing_modules = []
    for module in modules:
        if not importlib.util.find_spec(module):
            missing_modules.append(module)
    return missing_modules

def exit_if_dependencies_missing(modules):
    missing = check_dependencies(modules)
    if missing:
        print("Missing required modules:", missing)
        sys.exit(1)  # Exits the script with an error status

def is_ffmpeg_installed():
    try:
        # Try running a simple ffmpeg command and capture its output
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # CalledProcessError or FileNotFoundError means ffmpeg is not installed or not in PATH
        return False        

def clean_text(text):
    # Replace end-of-line hyphens with an empty string
    text = re.sub(r'-\n', '', text)
    # Replace line breaks within paragraphs with a space
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return text

# Function to convert MP3 to WAV
def convert_mp3_to_wav(mp3_file, wav_file, bit_depth):
    audio = AudioSegment.from_mp3(mp3_file)
    # audio.export(wav_file, format="wav")
    audio.export(wav_file, format="wav", parameters=["-acodec", "pcm_s16le" if bit_depth == 16 else "pcm_s24le"])

def read_text(read_text, region):
    engine = pyttsx3.init()
    engine.setProperty('voice', voices[region])  # replace `voice_id` with your chosen voice's ID
    engine.say (read_text)
    engine.runAndWait()

# Function to save text to speech using gTTS
def save_text(save_text, region, mp3_file):
    # Convert text to speech and save as MP3
    tts = gTTS(save_text, lang=lang_codes[region])
    tts.save(mp3_file)
    mp3_file_play = mp3_file
    # Convert the saved MP3 to WAV
    convert_mp3_to_wav(mp3_file, wav_filename, 16) #The default is set to 16-bit. 
    # larger bit depth = larger file and not better quality if the input is low quality like mp3.
    return mp3_file_play

def readPDF(ffile, fpage):
    # creating a PdfFileReader object 
    pdfReader = PyPDF2.PdfReader(ffile)
    # the page with which you want to start     
    from_page = pdfReader.pages[fpage]
    # extracting the text from the PDF 
    text = from_page.extract_text()
    # Clean the extracted text
    cleaned_text = clean_text(text)
    return cleaned_text

def play_mp3(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    # Play the MP3 file
    pygame.mixer.music.play()
    # Wait for the music to play before exiting
    while pygame.mixer.music.get_busy():
        time.sleep(1)

exit_if_dependencies_missing(required_modules)

# Check if ffmpeg is installed
if is_ffmpeg_installed():
    print("ffmpeg is installed.")
else:
    print("ffmpeg is not installed.")

# Extract base name for the output file
base_name = os.path.splitext(os.path.basename(path))[0]
mp3_filename = f"{base_name}.mp3"
wav_filename = f"{base_name}.wav"

# Read the PDF to text so it can be converted to voice
cleaned_text = readPDF(path, 0)

# uncomment to read the text to voice before save
# read_text(cleaned_text, user_choice)

# Save the text to voice and get the filename of the saved MP3
mp3_file_path = save_text(cleaned_text, user_choice, mp3_filename)

# uncomment to play the mp3 output
# play_mp3(mp3_file_path)
