from dis import dis
from turtle import up
from zlib import Z_PARTIAL_FLUSH
import cv2
from cv2 import drawChessboardCorners
from cv2 import blur
from matplotlib.pyplot import cla
import numpy as np
import time
from djitellopy import Tello
from pyimagesearch.pid import PID
import math

def auto_canny(image, sigma=0.33):
    # 計算單通道像素強度的中位數
    v = np.median(image)

    # 選擇合適的lower和upper值，然後應用它們
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    print(lower, upper)
    edged = cv2.Canny(image, lower, upper)

    return edged

def check(edge, hsv, u, d, l, r):
    if (edge[u:d, l:r] == 255).any():
        for i in range(u, d):
            for j in range(l, r):
                if (np.array([110,50,50]) < hsv[i][j]).all() and (hsv[i][j] < np.array([130, 255, 255])).all():
                    print("detect!")
                    return True
    return False

def clamp(x, max_speed_threshold = 50):
    if x > max_speed_threshold:
        x = max_speed_threshold
    elif x < -max_speed_threshold:
        x = -max_speed_threshold
    
    return x

def keyboard(self, key):
    print("key:", key)
    fb_speed = 40
    lf_speed = 40
    ud_speed = 50
    degree = 30
    if key == ord('1'):
        self.takeoff()
        time.sleep(3)
    if key == ord('2'):
        self.land()
    if key == ord('3'):
        self.send_rc_control(0, 0, 0, 0)
        print("stop!!!!")
    if key == ord('w'):
        self.send_rc_control(0, fb_speed, 0, 0)
        print("forward!!!!")
    if key == ord('s'):
        self.send_rc_control(0, (-1) * fb_speed, 0, 0)
        print("backward!!!!")
    if key == ord('a'):
        self.send_rc_control((-1) * lf_speed, 0, 0, 0)
        print("left!!!!")
    if key == ord('d'):
        self.send_rc_control(lf_speed, 0, 0, 0)
        print("right!!!!")
    if key == ord('z'):
        self.send_rc_control(0, 0, ud_speed, 0)
        print("down!!!!")
    if key == ord('x'):
        self.send_rc_control(0, 0, (-1) *ud_speed, 0)
        print("up!!!!")
    if key == ord('c'):
        self.send_rc_control(0, 0, 0, degree)
        print("rotate!!!!")
    if key == ord('v'):
        self.send_rc_control(0, 0, 0, (-1) *degree)
        print("counter rotate!!!!")
    if key == ord('5'):
        height = self.get_height()
        print(height)
    if key == ord('6'):
        battery = self.get_battery()
        print(battery)

drone = Tello()
drone.connect()
drone.streamon()
f = cv2.FileStorage("calibrate.xml", cv2.FILE_STORAGE_READ)
intrinsic = f.getNode("intrinsic").mat()
distortion = f.getNode("distortion").mat()
f.release()

x_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
y_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
z_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
yaw_pid = PID(kP=0.7, kI=0.0001, kD=0.1)

x_pid.initialize()
y_pid.initialize()
z_pid.initialize()
yaw_pid.initialize()

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
hasRead = False

dir_order = ["r", "u", "r", "u", "l", "d"]
control_dict = {
    "r": (10, 0, 0, 0),
    "u": (0, 0, 10, 0),
    "l": (-10, 0, 0, 0),
    "d": (0, 0, -20, 0),
}


while True:
    # break
    frame = drone.get_frame_read()
    frame = frame.frame
    cv2.imshow("", frame)
    key = cv2.waitKey(1)
    h, w = frame.shape[:2]
    markerCorners, markerids, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters = parameters)
    x_update = 0
    y_update = 0
    z_update = 0
    yaw_update = 0
    if markerids is not None and drone.is_flying:
        hasRead = True
        rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
        id = markerids[0][0]
        if id == 0:
            i = 0
            rotM = np.zeros(shape=(3, 3))
            cv2.Rodrigues(rvec[0], rotM, jacobian=0)
            x_update = (tvec[0,0,0] - (-10)) * 2
            y_update = -(tvec[0,0,1] - (-15)) * 1.5
            z_update = (tvec[0,0,2] - 30) * 0.5
            if abs(z_update) <= 17.5 and abs(x_update) <= 10:
                drone.send_rc_control(30, 0, 0, 0)
                time.sleep(1)
                drone.send_rc_control(0, 0, 0, 0)
                break
            x_update = clamp(x_pid.update(x_update, sleep=0))
            y_update = clamp(y_pid.update(y_update, sleep=0))
            z_update = clamp(z_pid.update(z_update, sleep=0))

            drone.send_rc_control(int(x_update), int(z_update), int(y_update), 0)
                
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerids)
            frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec[i,:,:], tvec[i,:,:], 10)
            cv2.putText(frame,"x = "+str(round(tvec[i,0,0], 2))+", y = "+str(round(tvec[i,0,1], 2))+", z = "+str(round(tvec[i,0,2], 2)), (0,64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2,cv2.LINE_AA)
            cv2.imshow("",frame)
            key = cv2.waitKey(1)
    elif drone.is_flying and hasRead == False:
        drone.send_rc_control(0, 0, 50, 0)
    elif drone.is_flying:
        drone.send_rc_control(0, 0, 0, 0)
    if key != -1:
        keyboard(drone, key)

for i, dir in enumerate(dir_order):
    while True:
        frame = drone.get_frame_read()
        frame = frame.frame
        markerCorners, markerids, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters = parameters)
        if markerids is not None and drone.is_flying and i == len(dir_order) - 1:
            drone.land()
            break
        key = cv2.waitKey(1)
        h, w = frame.shape[:2]
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, _ = frame.shape
        print(h, w)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edge_frame = auto_canny(blur_gray)
        edge_frame = cv2.dilate(edge_frame, (3, 3), 5)
        cv2.imshow("",edge_frame)
        if i != len(dir_order) - 1:
            next = dir_order[i+1]
            if next == "r":
                if check(edge_frame, hsv_frame, 260, 340, 850, 960):
                    break
            elif next == "l":
                if check(edge_frame, hsv_frame, 0, 50, 0, 60):
                    drone.send_rc_control(0, 10, 25, 0)
                    time.sleep(1.5)
                    drone.send_rc_control(-30, 0, 0, 0)
                    time.sleep(1.25)
                    drone.send_rc_control(0, 0, 0, 0)
                    break
            elif next == "u":
                if check(edge_frame, hsv_frame, 0, 40, 400, 560):
                    break
            elif next == "d":
                if check(edge_frame, hsv_frame, 680, 720, 400, 560):
                    break
        drone.send_rc_control(*control_dict[dir])
        if key != -1:
            keyboard(drone, key)
    
