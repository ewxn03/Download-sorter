import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import shutil
import logging


logging.basicConfig(filename='ChangeLog.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_mappings(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  

def save_mappings(filepath, mappings):
    with open(filepath, 'w') as file:
        json.dump(mappings, file)

def display_mappings(mappings):
    formatted_mappings = '\n'.join(f'{ext}: {folder}' for ext, folder in mappings.items())
    messagebox.showinfo("Current File Type Mappings", formatted_mappings)

def sort_downloads(directory, file_mappings):
    directory_path = os.path.abspath(directory)
    if not os.path.exists(directory_path):
        logging.error(f"The specified directory does not exist: {directory}")
        return

    for filename in os.listdir(directory_path):
        source = os.path.join(directory_path, filename)
        if os.path.isfile(source):
            ext = os.path.splitext(filename)[1].lower()
            if ext in file_mappings:
                dest_dir = os.path.join(directory_path, file_mappings[ext])
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.move(source, dest_dir)
                logging.info(f"Moved {filename} to {dest_dir}")

def add_mapping(mappings, filepath):
    extension = simpledialog.askstring("Input", "Enter file extension (e.g., .txt):")
    folder = simpledialog.askstring("Input", "Enter folder name:")
    if extension and folder:
        mappings[extension] = folder
        save_mappings(filepath, mappings)
        logging.info(f"Added new mapping: {extension} -> {folder}")
        messagebox.showinfo("Success", "Mapping added successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Download Organizer')
    file_mappings_path = 'file_mappings.json'
    file_mappings = load_mappings(file_mappings_path)

    tk.Button(root, text='Add File Type Mapping', command=lambda: add_mapping(file_mappings, file_mappings_path)).pack()
    tk.Button(root, text='Organize Now', command=lambda: sort_downloads(r'C:\Users\ewanm\Downloads', file_mappings)).pack()
    tk.Button(root, text='Show Current Mappings', command=lambda: display_mappings(file_mappings)).pack()

    root.mainloop()


