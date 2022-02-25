import numpy as np
from tqdm import tqdm
import cv2

    

img = cv2.imread("lisa.jpeg")

h, w = img.shape[0], img.shape[1]

res = np.zeros((3*h, 3*w, 3))

for i in tqdm(range(3*h)):
    for j in range(3*w):
        nx = i // 3 * 3
        ny = j // 3 * 3
        dx = (i - nx) / 3
        dy = (j - ny) / 3
        nx //= 3
        ny //= 3
        
        if nx + 1 >= h:
            px1 = (dx) * img[nx][ny]
        else:
            px1 = (dx) * img[nx][ny] + (1 - dx) * img[nx+1][ny]
            
        if ny + 1 >= w:
            px2 = np.array([0, 0, 0])
        else :
            if nx + 1 >= h:
                px2 = (dx) * img[nx][ny+1]
            else :
                px2 = (dx) * img[nx][ny+1] + (1 - dx) * img[nx+1][ny+1]
        
        res[i][j] = dy * px1 + (1-dy) * px2;

cv2.imwrite("lisa_bilinear.jpeg", res)
