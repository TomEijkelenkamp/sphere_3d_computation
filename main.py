# Created using chatgpt-4
import math
import cv2
import numpy as np

# Read the image
image = cv2.imread('sphere.png')  # Replace with your image path
image_1 = image.copy()
image_2 = image.copy()

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optionally apply Gaussian blur to smooth the image
gray = cv2.GaussianBlur(gray, (9, 9), 2)

# Perform Canny edge detection
edges = cv2.Canny(gray, 10, 50)

# Save the edges image
cv2.imwrite('edges.png', edges)

# Use Hough Circle Transform to find circles
# Parameters here are in the following order:
# 1. The input image.
# 2. The type of Hough Transform.
# 3. The inverse ratio of the accumulator resolution to the image resolution (dp).
# 4. The minimum distance between the centers of the detected circles.
# The two following values are the upper and lower thresholds for the Canny edge detector (higher values mean less circles detected).
# The next is the accumulator threshold for the circle centers at the detection stage (smaller values mean more circles, but increase false positives).
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=1000,
                            param1=10, param2=50, minRadius=50, maxRadius=0)


# Ensure at least some circles were found
if circles is not None:
    # Convert the circle parameters (x, y, radius) to integers
    circles = np.round(circles[0, :]).astype("int")

    # Loop over the circles
    (x, y, r) = circles[0]

    # Draw the outer circle
    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
    # Draw the center of the circle
    cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

    cv2.imwrite('circled.png', image)
    
    # Create a mask for the circle
    mask = np.zeros_like(gray)
    cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    
    # Bitwise-AND mask and original image
    masked_img = cv2.bitwise_and(gray, gray, mask=mask)
    
    # Find the brightest spot in the masked region
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(masked_img)
    
    # Draw the brightest spot on the original image
    cv2.circle(image, maxLoc, 5, (255, 0, 0), -1)

    cv2.imwrite('highlight.png', image)

    # Draw the line from the center to the brightest spot
    cv2.line(image, (x, y), maxLoc, (255, 0, 0), 2)

    cv2.imwrite('direction.png', image)

    (xh, yh) = maxLoc
    distance = math.sqrt((x - xh) ** 2 + (y - yh) ** 2)
    angle = round(distance / r * 90)
    print(f"Angle of the light vector with the z axis: {angle} degrees")
