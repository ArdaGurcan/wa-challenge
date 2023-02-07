import cv2
import numpy as np
  
# read the original image
img = cv2.imread("red.png")

# convert color range to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  

# set possible range for red color and choose values inside
upper_threshold = np.array([170, 120, 100])
max_val = np.array([180, 255, 255])
cone_mask = cv2.inRange(hsv, upper_threshold, max_val)

# create maks for left and right side of the image
right_mask = np.zeros(img.shape[:2], np.uint8)
left_mask = np.zeros(img.shape[:2], np.uint8)
right_mask[600:2420, 0:908] = 255
left_mask[600:2420, 908:1816] = 255

# combine masks with the mask containing cones
left_mask = cv2.bitwise_and(cone_mask, left_mask)
right_mask = cv2.bitwise_and(cone_mask, right_mask)

# for each mask
for mask in [left_mask, right_mask]:
  # get the white points
  points = np.argwhere(mask == 255)

  # fit a line to points in the map
  [vy,vx,y,x] = cv2.fitLine(points,cv2.DIST_L2,0,0.01,0.01)

  # find two extreme points on the line to draw line
  lefty = int((-x*vy/vx) + y)
  righty = int(((img.shape[1]-x)*vy/vx)+y)

  # add the line to image
  cv2.line(img,(img.shape[1]-1,righty),(0,lefty),(0,50,255),5)

# save image
cv2.imwrite('answer.png',img)