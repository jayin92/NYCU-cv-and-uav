from dis import dis
import cv2
from cv2 import drawChessboardCorners
import numpy as np
cap = cv2.VideoCapture(0)
pic = []

objp = np.zeros((9*6,3), np.float32)
# for i in range(6):
#     for j in range(9):
#         objp[i*9+j]=(i,j,0)

objp[:, :2]=np.mgrid[0:9, 0:6].T.reshape(-1, 2)
# print(objp)
objpoints = []
imgpoints = []
while len(objpoints) < 10:
    ret, frame = cap.read()
    h,w = frame.shape[:2]
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret2, corner = cv2.findChessboardCorners(gray_frame, (9,6))
    cv2.imshow("frame", frame)
    cv2.waitKey(33)
    if ret2:
        corner2 =  cv2.cornerSubPix(gray_frame,corner, (11,11), (-1,-1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1))
        objpoints.append(objp.copy())
        imgpoints.append(corner2)
        drawn_frame = drawChessboardCorners(frame, (9, 6), corner2, ret2)
        cv2.imshow("frame", drawn_frame)
        cv2.waitKey(33)

ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (h, w), None, None)
# f = cv2.FileStorage("calibrate.xml", cv2.FILE_STORAGE_WRITE)
# f.write("intrinsic", cameraMatrix)
# f.write("distortion", distCoeffs)
# f.release()

dictionary = cv2.aruco.Dinctionary_get(cv.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
while True:
    ret, frame = cap.read()
    cv2.imshow("",frame)
    cv2.waitKey(10)
    h, w = frame.shape[:2]
    intrinsic = cameraMatrix
    distortion = distCoeffs
    markerCorners, markerids, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters = parameters)
    frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerids)
    rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkerss(markerCorners, 15, intrinsic, distCoeffs)
    frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 0.1)