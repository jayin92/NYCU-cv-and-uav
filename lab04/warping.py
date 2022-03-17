import cv2
import numpy as np

h, w = 480, 640

bg = cv2.imread("broadway.jpg")

cap_corner = np.array([(0, 0), (479, 0), (479, 639), (0, 639)])
cap_corner = np.array([(0, 0), (479, 0), (479, 639), (0, 639)])
print(cap_cor)
cv2.imshow("figure", bg)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# print(frame.shape)

'''
427 207 top left
614 101 top right
633 421 bottom right
426 423 bottom left
'''