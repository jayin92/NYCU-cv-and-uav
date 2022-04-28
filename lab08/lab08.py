import cv2
import dlib
import numpy as np
from math import sqrt

def dis(tvec):
    return round(float(tvec[2]), 2)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture(0)
f = cv2.FileStorage("calibrate.xml", cv2.FILE_STORAGE_READ)
intrinsic = f.getNode("intrinsic").mat()
distortion = f.getNode("distortion").mat()

face_x = 14.5
# body_x = 75
body_y = 200
face_objPoints = np.float32([(0, 0, 0), (face_x, 0, 0), (face_x, face_x, 0), (0, face_x, 0)])

while True:
    _, src = cap.read()
    rects, weights = hog.detectMultiScale(src, winStride=(8, 8), scale=1.05, useMeanshiftGrouping = False)
    face_rects = detector(src, 0)
    for i, d in enumerate(face_rects):
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        # print(abs(x1-x2), abs(y1-y2))
        src = cv2.rectangle(src, (x1, y1), (x2, y2), (0, 0, 255), 2)
        imgPoints = np.float32([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
        _, _, tvec = cv2.solvePnP(face_objPoints, imgPoints, intrinsic, distortion)
        cv2.putText(src, str(dis(tvec)), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1, cv2.LINE_AA)
    for rect in rects:
        (x, y, w, h) = rect
        src = cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
        imgPoints = np.float32([(x, y), (x+w, y), (x+w, y+h), (x, y+h)])
        body_x = body_y / 2
        print(body_x, body_y)
        body_objPoints = np.float32([(0, 0, 0), (body_x, 0, 0), (body_x, body_y, 0), (0, body_y, 0)])
        _, _, tvec = cv2.solvePnP(body_objPoints, imgPoints, intrinsic, distortion)
        print(tvec)
        cv2.putText(src, str(dis(tvec)), (x+w, y+h), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow("t", src)
    cv2.waitKey(1)