import cv2
import numpy as np
from math import floor

img = cv2.imread("kifune.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

w, h = img.shape[0], img.shape[1]

total = w * h
cnt = np.zeros((256))
sum = np.zeros((256))

for i in range(w):
    for j in range(h):
        cnt[img[i][j][2]] += 1

cnt = cnt / total
for i in range(1, 256):
    cnt[i] += cnt[i-1]

cnt *= 255.0
cnt += 0.0001
cnt = list(map(floor, cnt))

for i in range(w):
    for j in range(h):
        img[i][j][2] = cnt[img[i][j][2]]

cv2.imwrite("kifune_result.jpg", cv2.cvtColor(img, cv2.COLOR_HSV2BGR))