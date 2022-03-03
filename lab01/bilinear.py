import numpy as np
from tqdm import tqdm
import cv2

    

img = cv2.imread("lisa.jpeg")

h, w = img.shape[0], img.shape[1]

pad = np.zeros((h+2, w+2, 3))

for i in range(h):
    for j in range(w):
        pad[i+1][j+1] = img[i][j]

res = np.zeros((3*h, 3*w, 3))

for i in range(3*h):
    for j in range(3*w):
        x = (i-1) // 3 + 1
        y = (j-1) // 3 + 1
        dx = i - (i-1) // 3 * 3
        dy = j - (j-1) // 3 * 3
        dx /= 3
        dy /= 3
        



cv2.imwrite("lisa_bilinear.jpeg", res)
