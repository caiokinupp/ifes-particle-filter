# import OpenCV
import cv2

# HSV color boundaries
corLower = (29, 86, 6)
corUpper = (64, 255, 255)

def getFrameContour(frame):
    # Reduce the size of the frame for optimize de workload
    #frame = imutils.resize(frame, width=1000) #600px

    # Blur the image to reduce the noise and make the image uniform
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert the frame to HSV color model
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Apply a mask to limit the boundariess, making the frame bonary
    mask = cv2.inRange(hsv, corLower, corUpper)

    # Reducing the imperfection removing bubbles and erosions of the frame
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Identifying the border of the mask
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Guarantee the openCV compatibility
    contour = contour[0] if imutils.is_cv2() else contour[1]
    return contorno
