import os
import cv2
import numpy as np
from PIL import Image as PILImage

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = filter_contours(contours)
    filtered_contours.sort(key=lambda c: cv2.boundingRect(c)[0])

    first_term = os.path.basename(image_path).split('+')[0].split('_')[1]

    cropped_images = []

    for i, c in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = image[y:y + h, x:x + w]
        cropped_pil_image = PILImage.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

        background = PILImage.new("RGBA", cropped_pil_image.size, (255, 255, 255))
        cropped_pil_image = cropped_pil_image.convert("RGBA")
        background.paste(cropped_pil_image, (0, 0), cropped_pil_image)
        cropped_pil_image = background.convert("RGB")

        cropped_images.append((cropped_pil_image, f"{first_term}_{i + 1}.png"))

    return cropped_images

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