import numpy as np
import cv2

def cal(n_b, n_o, miu_b, miu_o):
    return n_b * n_o * ((miu_b - miu_o) ** 2)

img = cv2.imread("input.jpg")

w, h = img.shape[0], img.shape[1]

cnt = np.zeros((256))

sum = 0

for i in range(w):
    for j in range(h):
        cnt[img[i][j][0]] += 1
        sum += img[i][j][0]
print(cnt)
n_b = cnt[0]
n_o = h * w - cnt[0]
miu_b = 0
miu_o = sum / n_o

best = cal(n_b, n_o, miu_b, miu_o)
thresh = 0


for i in range(1, 256):
    miu_b = (miu_b * n_b + cnt[i] * i) / (n_b + cnt[i])
    miu_o = (miu_o * n_o - cnt[i] * i) / (n_o - cnt[i])
    n_b += cnt[i]
    n_o -= cnt[i]
    print(n_b, n_o, miu_b, miu_o)

    cur = cal(n_b, n_o, miu_b, miu_o)
    if cur >= best:
        # print(cur)
        best = cur
        thresh = i

print(thresh)

for i in range(w):
    for j in range(h):
        img[i][j][:] = (0 if img[i][j][0] <= thresh else 255)

cv2.imwrite("otsu_result.jpg", img)