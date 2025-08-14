import cv2
import numpy as np

def detect_crops_and_trees(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to get a binary image
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image (for visualization)
    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    # Calculate the bounding box for each contour
    boxes = [cv2.boundingRect(cnt) for cnt in contours]

    return result, boxes

# Load the stitched image
stitched_image = cv2.imread('stitchedOutput1.png')

# Detect crops and trees
result, crop_tree_boxes = detect_crops_and_trees(stitched_image)

# Display the result
cv2.imshow('Crop and Tree Detection', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the bounding boxes of detected crops and trees
print("Detected Crop and Tree Boxes:")
for box in crop_tree_boxes:
    print(box)

# Save the image showing the detected areas outlined
cv2.imwrite('detected_areas.jpg', result)

def detect_disease(image):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of colors corresponding to the disease (you may need to adjust these values)
    lower_color = np.array([0, 50, 50])
    upper_color = np.array([10, 255, 255])

    # Create a mask using the specified color range
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Apply blurring and morphological operations to the mask
    blurred = cv2.GaussianBlur(mask, (11,11), 0)
    kernel = np.ones((5, 5), np.uint8)
    morphed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)

    # Find contours in the processed mask
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out contours that are too small or too large
    min_area = 100
    max_area = 1000
    detected_diseases = [cnt for cnt in contours if min_area < cv2.contourArea(cnt) < max_area and cv2.isContourConvex(cnt)]

    # Draw contours on the original image (for visualization)
    result_image = image.copy()
    cv2.drawContours(result_image, detected_diseases, -1, (0, 255, 0), 2)

    # Print debugging information
    print("Number of contours:", len(contours))
    print("Areas of contours:", [cv2.contourArea(cnt) for cnt in contours])

    # Return the detected diseases (contours) and the result image
    return detected_diseases, result_image




# Process each cropped image (assuming crop_tree_boxes contains the bounding boxes)
for box in crop_tree_boxes:
    x, y, w, h = box
    cropped_image = stitched_image[y:y+h, x:x+w]  # Crop the image to the bounding box
    diseases, result_image = detect_disease(cropped_image)
    # Further processing or analysis
    # Print or store the detected diseases for each cropped image
    print("Detected diseases for cropped image at ({},{}): {}".format(x, y, len(diseases)))

    # Display the result image (for visualization)
    # cv2.imshow('Disease Detection Result', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
cv2.imwrite('detected_diseases.jpg', result_image)