import os
import glob
import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog
from PIL import Image

def process_image(image_path, output_folder):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = [c for c in contours if cv2.contourArea(c) > 100]
    contours.sort(key=lambda c: cv2.boundingRect(c)[0])

    first_term = os.path.basename(image_path).split('+')[0].split('_')[1]

    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = image[y:y+h, x:x+w]
        cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        cropped_pil_image.save(os.path.join(output_folder, f"{first_term}_{i+1}.png"))

def select_input():
    input_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if input_path:
        input_label.config(text=input_path)

def select_output():
    output_path = filedialog.askdirectory()
    if output_path:
        output_label.config(text=output_path)

def process_input():
    input_path = input_label.cget("text")
    output_path = output_label.cget("text")
    if os.path.isfile(input_path):
        process_image(input_path, output_path)
    else:
        for file in glob.glob(os.path.join(input_path, "*.png")):
            process_image(file, output_path)

root = Tk()
root.title("PNG Letter Processor")

select_input_button = Button(root, text="Select Input", command=select_input)
input_label = Label(root, text="")
select_output_button = Button(root, text="Select Output", command=select_output)
output_label = Label(root, text="")
process_button = Button(root, text="Process", command=process_input)

select_input_button.grid(row=0, column=0, padx=10, pady=10)
input_label.grid(row=0, column=1, padx=10, pady=10)
select_output_button.grid(row=1, column=0, padx=10, pady=10)
output_label.grid(row=1, column=1, padx=10, pady=10)
process_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
