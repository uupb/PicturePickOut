import os
import glob
from tkinter import filedialog, messagebox
from tkinter import Toplevel, Canvas
from tkinter import *
from PIL import ImageTk
from PIL import Image as PILImage
from utils import save_last_selected_folder, load_last_selected_folder
from image_processing import process_image




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
    container.bind("<Configure>", lambda e: update_image_canvas(container, cropped_images))
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
    cropped_images = []

    if os.path.isfile(input_path):
        cropped_images.extend(process_image(input_path))
    else:
        for file in glob.glob(os.path.join(input_path, "*.png")):
            cropped_images.extend(process_image(file))

    display_previews(cropped_images)


def update_image_canvas(container, cropped_images):
    max_width = container.winfo_width()
    max_height = container.winfo_height()

    max_dimension = 800

    for i, (image, file_name) in enumerate(cropped_images):
        # Resize the image to a lower resolution
        width, height = image.size
        scale_ratio = max_dimension / max(width, height)
        if scale_ratio < 1:
            new_width = int(width * scale_ratio)
            new_height = int(height * scale_ratio)
            image = image.resize((new_width, new_height), PILImage.ANTIALIAS)

        # Create a thumbnail for the grid display
        image.thumbnail((128, 128))
        photo = ImageTk.PhotoImage(image)

    for i, (image, file_name) in enumerate(cropped_images):
        original_width, original_height = image.size
        scale_ratio = min(max_width / original_width, max_height / original_height)

        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)

        resized_image = image.resize((new_width, new_height), PILImage.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)

        image_label = container.grid_slaves(row=i // 5, column=i % 5)[0]
        if hasattr(image_label, "cached_photo"):
            # Use cached PhotoImage if available
            image_label.cached_photo.paste(resized_image)
        else:
            # Create a new PhotoImage and cache it
            image_label.cached_photo = ImageTk.PhotoImage(resized_image)
        image_label.config(image=image_label.cached_photo)
        image_label.image = image_label.cached_photo



root = Tk()
root.title("PNG Letter Cropper")

input_label = Label(root, text="Input PNG or folder", width=40, anchor="w")
input_label.grid(row=0, column=0, padx=10, pady=10)

input_button = Button(root, text="Browse", command=select_input)
input_button.grid(row=0, column=1, padx=10, pady=10)

output_label = Label(root, text="Outputfolder", width=40, anchor="w")
output_label.grid(row=1, column=0, padx=10, pady=10)

output_button = Button(root, text="Browse", command=select_output)
output_button.grid(row=1, column=1, padx=10, pady=10)

process_button = Button(root, text="Process", command=process_input)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
