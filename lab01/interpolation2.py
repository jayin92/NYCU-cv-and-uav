import numpy as np
import cv2
import math

img = cv2.imread("lisa.jpeg")
w = img.shape[0]
h = img.shape[1]

zoom = np.zeros((w,h,3), np.uint8)
wz = zoom.shape[0]
hz = zoom.shape[1]

print("original",w,h)
print("zoomed",wz,hz)

for i in range(wz):
    for j in range(hz):
        for k in range(3):
            if math.floor(i/3) != math.ceil(i/3):
                x = img[math.floor(i/3)+80][math.floor(j/3)+300][k]*(i/3-math.floor(i/3))+img[math.ceil(i/3)+80][math.floor(j/3)+300][k]*(math.ceil(i/3)-i/3)
                y = img[math.floor(i/3)+80][math.ceil(j/3)+300][k]*(i/3-math.floor(i/3))+img[math.ceil(i/3)+80][math.ceil(j/3)+300][k]*(math.ceil(i/3)-i/3)
            else :
                x = img[math.floor(i/3)+80][math.floor(j/3)+300][k]
                y = img[math.floor(i/3)+80][math.ceil(j/3)+300][k]
            if x!=y:
                zoom[i][j][k] = x*(j/3-math.floor(j/3))+y*(math.ceil(j/3)-j/3)
            else :
                zoom[i][j][k] = x
cv2.imshow('MY Image',zoom)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("lisa_result_2.jpg",zoom)

