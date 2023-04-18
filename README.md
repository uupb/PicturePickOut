# PicturePickOut
Supposed to scan output of stylized letters from another program and then separate each letter for use in yet another program 

still in progress only part built is PNG Letter Processeor which needs some dialing in still

Generated ReadMe below:

# PNG Letter Processor

PNG Letter Processor is a Python application that processes PNG images containing stylized letters on a blank background. It crops out each letter and saves them as separate image files.

## Features

- Simple graphical user interface (GUI) for selecting input files and output folder
- Processes single PNG files or all PNG files in a folder
- Automatically detects and crops letters from images
- Saves cropped letters with a custom filename format

## Installation

1. Clone the repository or download the source code:

git clone https://github.com/uupb/PNG-Letter-Processor.git


2. Install the required Python libraries:
pip install opencv-python
pip install Pillow


## Usage

1. Run the `main.py` script: python main.py

2. Click on the "Select Input" button to choose a single PNG file or a folder containing multiple PNG files.

3. Click on the "Select Output" button to choose the output folder where the cropped images will be saved.

4. Click on the "Process" button to process the input files. The application will automatically crop out each letter and save them in the selected output folder.




