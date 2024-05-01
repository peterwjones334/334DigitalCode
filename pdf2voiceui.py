import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def convert_pdf():
    pdf_path = file_path_entry.get()
    voice = voice_option.get()
    output_format = format_option.get()
    
    # Placeholder for conversion function
    # You would call your PDF to voice conversion function here
    print(f"Converting {pdf_path} with voice {voice} to {output_format} format.")
    
    messagebox.showinfo("Conversion Started", f"Converting {pdf_path} to {output_format}.")

# Set up the main tkinter window
root = tk.Tk()
root.title("PDF to Voice Converter")

# Create a frame for file selection
file_frame = ttk.Frame(root, padding="10")
file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# File path entry
file_path_entry = ttk.Entry(file_frame, width=50)
file_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

# File selection button
file_select_button = ttk.Button(file_frame, text="Select PDF", 
                                command=lambda: file_path_entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])))
file_select_button.grid(row=0, column=2)

# Voice selection
voice_option = tk.StringVar()
voice_label = ttk.Label(root, text="Choose Voice:")
voice_label.grid(row=1, column=0, sticky=tk.W, padx=10)
voice_combobox = ttk.Combobox(root, textvariable=voice_option, 
                              values=["UK Male", "UK Female", "US Male", "US Female"])
voice_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10)
voice_combobox.current(0)

# Output format selection
format_option = tk.StringVar(value="MP3")
format_label = ttk.Label(root, text="Output Format:")
format_label.grid(row=2, column=0, sticky=tk.W, padx=10)
format_combobox = ttk.Combobox(root, textvariable=format_option, 
                               values=["MP3", "WAV"])
format_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=10)
format_combobox.current(0)

# Convert button
convert_button = ttk.Button(root, text="Convert", command=convert_pdf)
convert_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)

# Run the application
root.mainloop()
