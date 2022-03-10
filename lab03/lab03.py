from itertools import count
import cv2
import numpy as np


def find_par(relation, i):
    if (i in relation) == False:
        return i
    else:
        return find_par(relation, relation[i])

def ConnectedComponents(img):
    h, w = img.shape
    label = []
    for i in range(h):
        label.append([0 for _ in range(w)])
    counter = 1
    relation = {}
    area = {}

    for i in range(h):
        for j in range(w):
            if img[i][j] == 255:
                if i >= 1 and j >= 1 and label[i-1][j] != 0 and label[i][j-1] != 0 and label[i-1][j] != label[i][j-1]:
                    label[i][j] = min(label[i-1][j], label[i][j-1])
                    relation[max(label[i-1][j], label[i][j-1])] = min(label[i-1][j], label[i][j-1])
                elif i>=1 and label[i-1][j] != 0:
                    label[i][j] = label[i-1][j]
                elif j>=1 and label[i][j-1] != 0:
                    label[i][j] = label[i][j-1]
                else:
                    label[i][j] = counter
                    counter += 1

    print(f"counter: {counter}")
    # Solving
    for i in range(h):
        for j in range(w):
            if label[i][j] == 0:
                continue
            label[i][j] = find_par(relation, label[i][j])
            area[label[i][j]] = 0
    
    for i in range(h):
        for j in range(w):
            if label[i][j] != 0:
                area[label[i][j]] += 1
    
    return label, area




cap = cv2.VideoCapture("vtest.mp4")

back = cv2.createBackgroundSubtractorMOG2()
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 15.0, (720, 576))


framen = 30
while cap.isOpened() and framen != 0:
    _, img = cap.read()
    h, w, _ = img.shape
    fgmask = back.apply(img)
    shadowVal = back.getShadowValue()
    ret, nmask = cv2.threshold(fgmask, shadowVal, 255, cv2.THRESH_BINARY)
    label, area = ConnectedComponents(nmask)
    candi = []
    for k, v in area.items():
        if v >= 350:
            candi.append(k)

    for item in candi:
        right = w
        left = 0
        top = h
        bottom = 0
        for i in range(h):
            for j in range(w):
                if label[i][j] == item:
                    right = min(right, j)
                    left = max(left, j)
                    top = min(top, i)
                    bottom = max(bottom, i)
        cv2.rectangle(img, (right, top), (left, bottom), (0, 255, 0))           
    out.write(img)

out.release()

    