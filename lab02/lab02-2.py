import numpy as np
import cv2
import math

img = cv2.imread("input.jpg")
w = img.shape[0]
h = img.shape[1]
new = np.zeros((w,h,3), np.uint8)
x = np.zeros((256))
m = 0
k = 0
    
for i in range(w):
    for j in range(h):
        x[img[i][j][2]]+=1

for i in range(256):
    sum1 = 0
    mean1 = 0
    mean2 = 0
    for j in range(i+1):
        sum1 +=x[j]
    
    sum2 = w*h-sum1
    for j in range(i+1):
        mean1+=x[j]
        if mean1>=(sum1)/2:
            mean1=j
            break
    for j in range(i+1,256):
        mean2+=x[j]
        if mean2>=(sum2)/2:
            mean2=j
            break
    if m<sum1*sum2*((mean1-mean2)**2):
        m=sum1*sum2*((mean1-mean2)**2)
        k=i
        print(k,mean1,mean2)

for i in range(w):
    for j in range(h):
        if img[i][j][2]>=i:
            new[i][j][:]=255
        else:
            new[i][j][:]=0

cv2.imwrite("lab02-2result.jpg",new)