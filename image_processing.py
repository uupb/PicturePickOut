import os
import cv2
import numpy as np
from PIL import Image as PILImage

def process_image(image_path, min_distance):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    masked_image = apply_mask(image, min_distance)
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = filter_contours(contours)
    filtered_contours.sort(key=lambda c: cv2.boundingRect(c)[0])

    first_term = os.path.basename(image_path).split('+')[0].split('_')[1]

    cropped_images = []

    for i, c in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(c)
        cropped_image = image[y:y + h, x:x + w]
        cropped_pil_image = PILImage.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGBA))

        cropped_images.append((cropped_pil_image, f"{first_term}_{i + 1}.png"))

    return cropped_images

def apply_mask(image, min_distance):
    # Extract the alpha channel from the image
    alpha_channel = image[:, :, 3]

    # Create a binary mask using the alpha channel
    _, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

    # Apply morphological operations (dilation followed by erosion) to improve the mask
    kernel_size = int(min_distance / 2)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)

    # Apply the mask to the image so that only the shapes of interest are visible
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    return masked_image

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
