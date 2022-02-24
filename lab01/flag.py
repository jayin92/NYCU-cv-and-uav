import numpy as np
import cv2

img = cv2.imread("nctu_flag.jpg")

w = img.shape[0]
h = img.shape[1]

print(w, h)

for i in range(w):
    for j in range(h):
        if img[i][j][0] > 75 and img[i][j][0] * 0.8 > img[i][j][1] and img[i][j][0] * 0.8 > img[i][j][2]:
            continue
        else:
            img[i][j][:] = (int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])) / 3

cv2.imwrite("nctu_flag_result.jpg", img)
