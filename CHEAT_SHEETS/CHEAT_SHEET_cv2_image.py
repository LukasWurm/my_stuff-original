"""
OpenCV Library Cheat Sheet
===========================
This script demonstrates the basic usage of the OpenCV library in Python, 
which is used for image processing and computer vision tasks.
"""

import cv2  # Importing the OpenCV library

# -------------------------
# Reading and Displaying Images
# -------------------------

# Reading an image from file
image = cv2.imread('example.jpg')

# Displaying the image in a window
cv2.imshow('Displayed Image', image)

# Waits for a key press and closes the window
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------
# Converting Color Spaces
# -------------------------

# Converting the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Displaying the grayscale image
cv2.imshow('Grayscale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------
# Drawing Shapes on Images
# -------------------------

# Drawing a rectangle on the image (top-left corner, bottom-right corner, color, thickness)
cv2.rectangle(image, (50, 50), (200, 200), (0, 255, 0), 3)

# Drawing a circle on the image (center, radius, color, thickness)
cv2.circle(image, (150, 150), 50, (255, 0, 0), 2)

# Displaying the image with shapes
cv2.imshow('Image with Shapes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------
# Image Thresholding
# -------------------------

# Applying binary thresholding
_, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Displaying the thresholded image
cv2.imshow('Thresholded Image', thresh_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------
# Edge Detection using Canny
# -------------------------

# Performing Canny edge detection
edges = cv2.Canny(gray_image, 100, 200)

# Displaying the edges
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
