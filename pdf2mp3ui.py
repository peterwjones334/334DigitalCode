# This code provides an interface to convert .pdf to .mp3 
# importing the modules
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from gtts import gTTS, gTTSError
import re
import PyPDF2
import pygame
from pydub import AudioSegment

output_mp3_path = ""  # Global variable to store the full path of the output MP3 file

def check_gtts_connectivity():
    try:
        # Attempt a small TTS conversion
        test_tts = gTTS("test", lang='en')
        test_tts.save("test.mp3")
        os.remove("test.mp3")  # Clean up the test file
        return True
    except gTTSError as e:
        print(f"gTTS connectivity check failed: {e}")
        return False

def read_pdf(file_path, page_num=0):

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
    return text

def clean_text(text):

    # Example: replace end-of-line hyphens with an empty string and remove extra spaces
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def text_to_speech(text, lang='en', output_file='output.mp3'):

    tts = gTTS(text, lang=lang)
    tts.save(output_file)

def play_mp3():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(output_mp3_path.replace('/', os.sep).replace('\\', os.sep))
        pygame.mixer.music.play()
        stop_button.config(state=tk.NORMAL)  # Enable the stop button when playing
    except pygame.error as e:
        status_label.config(text=f"Error playing file: {e}")
    # You may want to handle the end of the playback or looping the playback as needed.

def stop_mp3():
    pygame.mixer.music.stop()
    stop_button.config(state=tk.DISABLED)  # Disable the stop button once stopped

def convert_mp3_to_wav(mp3_file_path):
    wav_file_path = mp3_file_path.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def start_conversion():

    # Check gTTS connectivity first
    if not check_gtts_connectivity():
        status_label.config(text="gTTS connectivity check failed. Please check your internet connection.")
        return
            
    global output_mp3_path
    # Reset the status label for a new conversion
    status_label.config(text="Converting...")

    pdf_path = file_path_entry.get().strip()
    # Check if the PDF file path is empty
    if not pdf_path:
        status_label.config(text="Please select a PDF file.")
        return
    page_num = int(page_num_entry.get())
    language = lang_option.get()
    output_file_name = output_file_entry.get().strip()

    if not output_file_name:
        status_label.config(text="Please enter a name for the output file.")
        return

    # If no directory is specified in output_file_name, use the same directory as the PDF
    if not os.path.dirname(output_file_name):
        pdf_dir = os.path.dirname(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_mp3_path = os.path.join(pdf_dir, base_name + '.mp3')
    else:
        output_mp3_path = output_file_name

    # Call the PDF reading module
    text = read_pdf(pdf_path, page_num)
    cleaned_text = clean_text(text)

    # Call the TTS conversion module
    text_to_speech(cleaned_text, lang=language, output_file=output_file_name)
    
    output_mp3_path = output_file_name  # Update the path after successful creation

    # Update the status label
    if convert_to_wav_var.get() == 1:
        # Convert the MP3 to WAV
        wav_file_path = convert_mp3_to_wav(output_mp3_path)
        status_label.config(text=f"Conversion completed. MP3 and WAV saved as {output_mp3_path} and {wav_file_path}")
    else:
        status_label.config(text=f"Conversion completed. MP3 saved as {output_mp3_path}")
    play_button.config(state=tk.NORMAL)  # Enable the play button


def show_help():
    help_text = (
        "PDF to Voice Converter Help\n\n"
        "Select PDF: Click to choose a PDF file.\n\n"
        "Page Number: Enter the page number in the PDF you want to convert to voice (starting from 0).\n\n"
        "Language: Select the language for the text-to-speech conversion.\n\n"
        "Output File Name: Enter the name for the output audio file (default extension is .mp3).\n\n"
        "Convert to WAV: Tick to additionally convert the .mp3 to .wav \n\n"
        "Convert: Click to start the conversion process.\n\n"
        "Play MP3: Click to play the converted audio file.\n\n"
        "Stop MP3: Click to stop the play of the converted audio file.\n\n"
        "Note: Ensure you have an active internet connection for the conversion."
    )
    messagebox.showinfo("Help - PDF to Voice Converter", help_text)    

root = tk.Tk()
root.title("PDF to Voice Converter")

# PDF file selection
file_path_entry = ttk.Entry(root, width=40)
file_path_entry.grid(row=0, column=1)
ttk.Button(root, text="Select PDF", command=select_pdf).grid(row=0, column=2)

# Page number
ttk.Label(root, text="Page Number:").grid(row=1, column=0)
page_num_entry = ttk.Entry(root)
page_num_entry.grid(row=1, column=1)
page_num_entry.insert(0, '0')  # Set default value to 0

# Language selection
ttk.Label(root, text="Language:").grid(row=2, column=0)
lang_option = ttk.Combobox(root, values=["en", "es", "fr"])
lang_option.grid(row=2, column=1)
lang_option.current(0)

# Output file name
ttk.Label(root, text="Output File Name:").grid(row=3, column=0)
output_file_entry = ttk.Entry(root)
output_file_entry.grid(row=3, column=1)
output_file_entry.insert(0, 'output.mp3')  # Set default value to 'output.mp3'

# Checkbox for MP3 to WAV conversion
convert_to_wav_var = tk.IntVar()
convert_to_wav_checkbox = ttk.Checkbutton(root, text="Convert to WAV", variable=convert_to_wav_var)
convert_to_wav_checkbox.grid(row=4, column=1, pady=5)

# Start conversion button
ttk.Button(root, text="Convert", command=start_conversion).grid(row=5, column=1)

# Status label for updates
status_label = ttk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=2)

# Button to play the MP3 file
play_button = ttk.Button(root, text="Play MP3", command=play_mp3, state=tk.DISABLED)
play_button.grid(row=7, column=1, pady=5)

# Stop button for stopping the MP3 playback
stop_button = ttk.Button(root, text="Stop MP3", command=stop_mp3, state=tk.DISABLED)
stop_button.grid(row=8, column=1, pady=5)

# Help button
help_button = ttk.Button(root, text="Help", command=show_help)
help_button.grid(row=9, column=1, pady=5)

root.mainloop()