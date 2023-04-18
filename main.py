import os
import glob
from tkinter import filedialog, messagebox
from tkinter import *
from utils import save_last_selected_folder, load_last_selected_folder
from image_processing import process_image

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
