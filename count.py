import cv2
import numpy as np

# Load the filtered image
filtered_image = cv2.imread('filtered_green_image.png')

# Convert the image to grayscale
gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

# Apply a binary threshold to create a binary image
_, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

# Find contours of the green objects
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Set a minimum area threshold to ignore very small green objects
min_area_threshold = 2000  # Adjust this value based on the object size
large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]

# Count the number of large green objects
large_green_objects_count = len(large_contours)

print("Number of large green objects:", large_green_objects_count)
