import cv2
import numpy as np

img = cv2.imread("lisa.jpeg")

h = img.shape[0]
w = img.shape[1]
print(img.shape)
res = np.zeros((3*h, 3*w, 3))

for i in range(h):
    for j in range(w):
        for x in range(3):
            for y in range(3):
                res[3*i+x][3*j+y] = img[i][j]

cv2.imwrite("lisa_nearest_neighbor.jpeg", res)

cv2.waitKey(0)
cv2.destroyAllWindows()