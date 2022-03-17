import cv2
import numpy as np

h, w = 640, 480

bg = cv2.imread("broadway.jpg")

cap_corner = np.float32([(0, 0), (h-1, 0), (h-1, w-1), (0, w-1)])
img_corner = np.float32([(427, 207), (614, 101), (633, 421), (426, 423)])
print(cap_corner.shape)
m = cv2.getPerspectiveTransform(cap_corner, img_corner)
cap = cv2.VideoCapture(0)
res = np.ones((3, h*w))
for i in range(h):
    for j in range(w):
        res[0][i*w+j] = i
        res[1][i*w+j] = j
        res[2][i*w+j] = 1
res = np.matmul(m, res)
# print(bg.shape)
while True:
    _, frame = cap.read()
    for i in range(h):
        for j in range(w):
            x = int(res[0, w*i+j] / res[2, w*i+j])
            y = int(res[1, w*i+j] / res[2, w*i+j])
            bg[y][x][:] = frame[j][i][:]

    cv2.imshow("t", bg)
    cv2.waitKey(33)
# print(frame.shape)
