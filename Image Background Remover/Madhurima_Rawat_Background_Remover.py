'''

Dependencies:

opencv, pillow, numpy

To install:

!pip install opencv-python Pillow numpy

'''


import cv2
import numpy as np
from PIL import Image

def remove_background(image_path):
    # Step 1: Read the image using PIL (Pillow)
    img = np.array(Image.open(image_path))

    # Step 2: Create a mask and initialize it as 'unknown' (2)
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[:, :] = 2

    # Step 3: Define a rectangle around the object to help GrabCut segment the image
    rect = (50, 50, img.shape[1]-80, img.shape[0]-80)

    # Step 4: Initialize the foreground and background models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Step 5: Apply GrabCut algorithm
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Step 6: Modify the mask to separate foreground (3) and probable foreground (1)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Step 7: Apply the mask to the original image
    result = img * mask2[:, :, np.newaxis]

    # Step 8: Display the original image and the result
    cv2.imshow(img)
    cv2.imshow(result)

if __name__ == "__main__":

    # Step 9: Replace image_path is the image path
    # First checking with lighthouse image
    image_path = '/content/Light House Sample Image.jpg'
    remove_background(image_path)