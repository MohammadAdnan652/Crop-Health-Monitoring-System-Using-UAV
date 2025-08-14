import cv2
import numpy as np

# Load the image
image = cv2.imread('stitchedOutput1.png')

# Convert the image to HSV (Hue, Saturation, Value) color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the green color range in HSV
lower_green = np.array([35, 40, 40])
upper_green = np.array([85, 255, 255])

# Create a mask for green color
mask = cv2.inRange(hsv, lower_green, upper_green)

# Apply the mask to keep only green regions in the image
filtered_image = cv2.bitwise_and(image, image, mask=mask)

# Save the filtered image
cv2.imwrite('filtered_green_image.png', filtered_image)
