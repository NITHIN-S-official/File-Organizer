import os
import shutil
from tkinter import Tk, filedialog, Button, Label
from datetime import datetime

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".avi", ".mov"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Others": []
}

SAFE_FOLDERS = ["Downloads", "Documents", "Desktop", "test folder"]

def organize_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            mod_time = os.path.getmtime(file_path)
            date_folder = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
            moved = False

            for category, extensions in FILE_TYPES.items():
                if file_ext in extensions:
                    dest = os.path.join(folder_path, category, date_folder)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest, filename))
                    moved = True
                    break

            if not moved:
                dest = os.path.join(folder_path, "Others", date_folder)
                os.makedirs(dest, exist_ok=True)
                shutil.move(file_path, os.path.join(dest, filename))

def check_safe_folder(folder_path):
    """Function to check if the folder is safe."""
    if not any(safe in folder_path for safe in SAFE_FOLDERS):
        status_label.config(text="Please select a safe folder (Downloads, Documents, etc.)")
        return False
    return True

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        if check_safe_folder(folder):  # Check if folder is safe before organizing
            organize_files(folder)
            status_label.config(text="Files organized successfully!")

root = Tk()
root.title("Smart File Organizer")
root.geometry("350x180")
Label(root, text="Smart File Organizer", font=("Arial", 14, "bold")).pack(pady=10)
Button(root, text="Select Folder to Organize", command=select_folder, height=2, width=25).pack(pady=10)
status_label = Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
