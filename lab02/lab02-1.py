import numpy as np
import cv2
import math

img = cv2.imread("kifune.jpg")
w = img.shape[0]
h = img.shape[1]
new = np.zeros((w,h,3),np.uint8)
x = np.zeros((256))
image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
s=0

for i in range(w):
    for j in range(h):
        x[image[i][j][2]]+=1

for i in range(256):
    s+=float (x[i]/(w*h))
    x[i]=int (s*255)

for i in range(w):
    for j in range(h):
        new[i][j][0]=image[i][j][0]
        new[i][j][1]=image[i][j][1]
        new[i][j][2]=x[image[i][j][2]]
new = cv2.cvtColor(new, cv2.COLOR_HSV2BGR)
cv2.imwrite("kifune_result.jpg",new)