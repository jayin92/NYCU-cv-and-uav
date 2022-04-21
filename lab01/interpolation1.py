import numpy as np
import cv2

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
            zoom[i][j][k] = img[round(i/3)+80][round(j/3)+300][k]

cv2.imshow('MY Image',zoom)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("lisa_result_1.jpg",zoom)

