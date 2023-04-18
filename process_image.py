'''

DEPRECIATED, SAVED IN CASE I MISS SOMETHING

import os
import glob
import cv2
import numpy as np
from PIL import Image as PILImage
from tkinter import filedialog, messagebox
from tkinter import *


def save_last_selected_folder(folder_path):
    with open("last_selected_folder.txt", "w") as f:
        f.write(folder_path)


def load_last_selected_folder():
    if os.path.exists("last_selected_folder.txt"):
        with open("last_selected_folder.txt", "r") as f:
            return f.read()
    return ""


def process_image(image_path, output_folder):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = filter_contours(contours)
    filtered_contours.sort(key=lambda c: cv2.boundingRect(c)[0])

    first_term = os.path.basename(image_path).split('+')[0].split('_')[1]

    for i, c in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = image[y:y+h, x:x+w]
        cropped_pil_image = PILImage.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

        background = PILImage.new("RGBA", cropped_pil_image.size, (255, 255, 255))
        cropped_pil_image = cropped_pil_image.convert("RGBA")
        background.paste(cropped_pil_image, (0, 0), cropped_pil_image)
        cropped_pil_image = background.convert("RGB")

        cropped_pil_image.save(os.path.join(output_folder, f"{first_term}_{i+1}.png"))


def filter_contours(contours):
    filtered_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        _, _, w, h = cv2.boundingRect(c)

        aspect_ratio = float(w) / h
        is_large_area = area > 100
        is_reasonable_aspect_ratio = 0.2 < aspect_ratio < 5

        if is_large_area and is_reasonable_aspect_ratio:
            filtered_contours.append(c)
    return filtered_contours


def select_input():
    input_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("PNG files", "*.png")])
    if input_path:
        input_label.config(text=input_path)


def select_output():
    output_path = filedialog.askdirectory(initialdir=load_last_selected_folder())
    if output_path:
        output_label.config(text=output_path)
        save_last_selected_folder(output_path)


def process_input():
    input_path = input_label.cget("text")
    output_path = output_label.cget("text")
    if os.path.isfile(input_path):
        process_image(input_path, output_path)
    else:
        for file in glob.glob(os.path.join(input_path, "*.png")):
            process_image(file, output_path)
    messagebox.showinfo("Success", "Image(s) processed successfully.")



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

'''
