import numpy as np
import cv2

img = cv2.imread("lisa.jpeg")

h, w = img.shape[0], img.shape[1]

res = cv2.resize(img, (3*w, 3*h), interpolation=cv2.INTER_LINEAR)

cv2.imwrite("lisa_bilinear_cv2.jpeg", res)