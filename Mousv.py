import cv2

import imutils

import numpy as np

import pytesseract

from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera






camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
              gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale

gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise

edged = cv2.Canny(gray, 30, 200) #Perform Edge detection


# find contours in the edged image, keep only the largest

# ones, and initialize our screen contour

cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

screenCnt = None


# loop over our contours

for c in cnts:

 # approximate the contour

 peri = cv2.arcLength(c, True)

 approx = cv2.approxPolyDP(c, 0.018 * peri, True)

 

 # if our approximated contour has four points, then

 # we can assume that we have found our screen

 if len(approx) == 4:

  screenCnt = approx

  break


 


if screenCnt is None:

 detected = 0

 print "No contour detected"

else:

 detected = 1


if detected == 1:

 cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)


# Masking the part other than the number plate

mask = np.zeros(gray.shape,np.uint8)

new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)

new_image = cv2.bitwise_and(image,image,mask=mask)


# Now crop

(x, y) = np.where(mask == 255)

(topx, topy) = (np.min(x), np.min(y))

(bottomx, bottomy) = (np.max(x), np.max(y))

Cropped = gray[topx:bottomx+1, topy:bottomy+1]


 


#Read the number plate

text = pytesseract.image_to_string(Cropped, config='--psm 11')

print("Detected Number is:",text)


cv2.imshow('image',image)

cv2.imshow('Cropped',Cropped)


cv2.waitKey(0)

cv2.destroyAllWindows()




