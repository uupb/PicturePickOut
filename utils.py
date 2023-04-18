import os

def save_last_selected_folder(folder_path):
    with open("last_selected_folder.txt", "w") as f:
        f.write(folder_path)

def load_last_selected_folder():
    if os.path.exists("last_selected_folder.txt"):
        with open("last_selected_folder.txt", "r") as f:
            return f.read()
    return ""
