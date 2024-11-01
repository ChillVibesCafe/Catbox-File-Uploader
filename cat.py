import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Catbox API endpoint for file uploads
API_URL_CATBOX = "https://catbox.moe/user/api.php"

# History file to store past uploads
HISTORY_FILE = "upload_history.json"

# Load history if exists
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

# Save history
def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

# Add to history
def add_to_history(url, note):
    history = load_history()
    history.append({"url": url, "note": note})
    save_history(history)

# Function to upload the file
def upload_file():
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename()
    if not file_path:
        logging.debug("No file selected by the user.")
        return  # No file selected
    
    try:
        # Open the selected file in binary mode
        with open(file_path, 'rb') as file:
            files = {'fileToUpload': file}
            params = {
                'reqtype': 'fileupload',
                'userhash': ''  # Optional user hash
            }
            # Log the parameters being sent
            logging.debug(f"Uploading file without expiration: {file_path}")
            logging.debug(f"Params: {params}")
            
            # Send POST request to upload the file to Catbox (permanent storage)
            response = requests.post(API_URL_CATBOX, files=files, data=params)

            # Log the response details
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response text: {response.text}")

            if response.status_code == 200:
                # If successful, show the URL in the GUI for easy copy-pasting
                upload_url = response.text.strip()
                result_label_var.set("Uploaded File URL:")
                result_entry.delete(0, tk.END)
                result_entry.insert(0, upload_url)
                # Ask user for a note to save with the URL
                note = simpledialog.askstring("Add Note", "Add a note for this upload:")
                if note is None:
                    note = ""
                add_to_history(upload_url, note)
            else:
                messagebox.showerror("Upload Failed", f"Error: {response.status_code}: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to view upload history
def view_history():
    history = load_history()
    history_window = tk.Toplevel(root)
    history_window.title("Upload History")
    history_window.geometry("600x400")
    history_window.configure(bg="#e6f7ff")
    
    title_label = tk.Label(history_window, text="Upload History", font=("Helvetica", 16, "bold"), bg="#e6f7ff", fg="#333333")
    title_label.pack(pady=10)
    
    frame = ttk.Frame(history_window, padding="15")
    frame.pack(expand=True, fill="both")
    
    text_widget = tk.Text(frame, wrap="word", font=("Arial", 12))
    text_widget.pack(expand=True, fill="both")
    
    for item in history:
        text_widget.insert(tk.END, f"URL: {item['url']}\nNote: {item['note']}\n\n")
    text_widget.config(state=tk.DISABLED)

# Function to handle the quit action
def quit_app():
    root.quit()

# Creating the Tkinter GUI
root = tk.Tk()
root.title("Catbox Uploader")
root.geometry("600x400+200+200")  # Set a fixed size window with specific placement
root.resizable(False, False)  # Disable window resizing
root.configure(bg="#e6f7ff")  # Soft blue background for better visual appeal

# Add a title banner
title_label = tk.Label(root, text="Catbox File Uploader", font=("Helvetica", 20, "bold"), bg="#e6f7ff", fg="#333333")
title_label.pack(pady=10)

# Create a stylish frame for content
frame = ttk.Frame(root, padding="15")
frame.pack(expand=True, fill="both")
frame.configure(style="My.TFrame")

# Create a file upload button
upload_button = ttk.Button(frame, text="Upload File", command=upload_file)
upload_button.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

# Label to display the URL information
result_label_var = tk.StringVar(value="Uploaded File URL:")
result_label = ttk.Label(frame, textvariable=result_label_var, font=("Arial", 12))
result_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

# Entry to display the upload result (URL) with easy copy-pasting
result_entry = ttk.Entry(frame, width=60, font=("Arial", 12))
result_entry.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

# Create a history button
history_button = ttk.Button(frame, text="View History", command=view_history)
history_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

# Create a quit button
quit_button = ttk.Button(frame, text="Quit", command=quit_app)
quit_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")

# Add a style to improve visual appeal
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TFrame", background="#e6f7ff")
style.configure("TLabel", background="#e6f7ff", font=("Arial", 12))

# Add styling to the buttons for a better look
style.map("TButton",
          background=[('active', '#66b3ff'), ('!disabled', '#99ccff')],
          relief=[('pressed', 'groove'), ('!pressed', 'ridge')])

# Start the GUI main loop
root.mainloop()
