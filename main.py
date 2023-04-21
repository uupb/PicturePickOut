import os
import glob
import threading

from tkinter import filedialog, messagebox
from tkinter import Toplevel, Canvas
from tkinter import *

from PIL import ImageTk
from PIL import Image as PILImage

from utils import save_last_selected_folder, load_last_selected_folder
from image_processing import process_image

# Global
min_distance = 50


def select_input():
    def open_file_dialog():
        return filedialog.askopenfilename(initialdir=load_last_selected_folder('input'), filetypes=[("PNG files", "*.png")])

    def open_directory_dialog():
        return filedialog.askdirectory(initialdir=load_last_selected_folder('input'))

    input_path = open_file_dialog() or open_directory_dialog()
    if input_path:
        input_label.config(text=input_path)
        save_last_selected_folder(input_path, 'input')


def select_output():
    output_path = filedialog.askdirectory(initialdir=load_last_selected_folder('output'))
    if output_path:
        output_label.config(text=output_path)
        save_last_selected_folder(output_path, 'output')


def display_previews(cropped_images):
    preview_window = Toplevel(root)
    preview_window.title("Image Previews")

    canvas = Canvas(preview_window)
    canvas.pack(side=LEFT, expand=True, fill=BOTH)

    scrollbar = Scrollbar(preview_window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    container = Frame(canvas)
    canvas.create_window(0, 0, anchor=NW, window=container)

    selected_images = set()

    def on_image_click(event, index):
        if index in selected_images:
            selected_images.remove(index)
            event.widget.config(borderwidth=2, relief="sunken")
        else:
            selected_images.add(index)
            event.widget.config(borderwidth=2, relief="raised")

    for i, (image, file_name) in enumerate(cropped_images):
        image.thumbnail((128, 128))
        photo = ImageTk.PhotoImage(image)

        image_label = Label(container, image=photo, borderwidth=2, relief="sunken")
        image_label.grid(row=i // 5, column=i % 5, padx=10, pady=10)
        image_label.image = photo
        image_label.bind("<Button-1>", lambda e, idx=i: on_image_click(e, idx))

    def save_selected_images():
        output_folder = output_label.cget("text")
        for i, (image, file_name) in enumerate(cropped_images):
            if i in selected_images:
                image.save(os.path.join(output_folder, file_name))
        preview_window.destroy()
        messagebox.showinfo("Success", "Image(s) processed successfully.")

    save_button = Button(preview_window, text="Save Selected", command=save_selected_images)
    save_button.pack(pady=10)


def process_input():
    input_path = input_label.cget("text")
    output_path = output_label.cget("text")

    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select input and output folders.")
        return

    cropped_images = []


    if os.path.isfile(input_path):
        try:
            cropped_images.extend(process_image(input_path, min_distance))
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {input_path}\n{e}")
            return
    else:
        for file_path in glob.glob(os.path.join(input_path, "*.png")):
            try:
                cropped_images.extend(process_image(file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {file_path}\n{e}")
                return

    if cropped_images:
        root.after(0, lambda: display_previews(cropped_images))
    else:
        messagebox.showinfo("No Images Found", "No .png images found in the input folder.")


def select_images():
    folder_path = filedialog.askdirectory()
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    cropped_images = []
    for image_path in image_paths:
        cropped_images.extend(process_image(image_path))

    return cropped_images


def process_images_thread():
    input_path = input_label.cget("text")
    output_path = output_label.cget("text")
    cropped_images = []

    if os.path.isfile(input_path):
        try:
            cropped_images.append(process_image(input_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error processing file: {input_path}\n{e}")
            return
    else:
        for file_path in glob.glob(os.path.join(input_path, "*.png")):
            try:
                cropped_images.append((PILImage.open(file_path), os.path.basename(file_path)))
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file: {file_path}\n{e}")
                return

    if cropped_images:
        root.after(0, lambda: display_previews(cropped_images))
    else:
        messagebox.showinfo("No Images Found", "No .png images found in the input folder.")


root = Tk()
root.title("Picture Pick Out")

input_button = Button(root, text="Select Input Folder or File", command=select_input)
input_button.pack(pady=10)

input_label = Label(root, text="")
input_label.pack(pady=5)

output_button = Button(root, text="Select Output Folder", command=select_output)
output_button.pack(pady=10)

output_label = Label(root, text="")
output_label.pack(pady=5)

process_button = Button(root, text="Process Images", command=process_input)
process_button.pack(pady=10)

root.mainloop()

