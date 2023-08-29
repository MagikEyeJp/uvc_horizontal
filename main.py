#!/usr/bin/env python3

from cv2 import WINDOW_FULLSCREEN
import numpy as np
import cv2 as cv
import subprocess as ss
import sys
import os
import datetime as dt
import time

LOG_DIR = "/home/pi/Desktop/saved_image/"
FLG_GRID = False
FLG_STRB = False
STRB_ON = True
STRB_OFF = False
LINE_COLOR = (0,0,255)
WIDTH = 640
HEIGHT = 480
ZOOM_MAX = 5
ZOOM_REF = 1.2

CMD_STRB_ON = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=1"
CMD_STRB_OFF = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=0"
CMD_SET_EXPOSURE_REF = "v4l2-ctl -d 0 --set-ctrl=auto_exposure_reference=80"
CMD_SET_EXPOSURE_AUTO = "v4l2-ctl -d 0 --set-ctrl=exposure_auto_upper_limit_us=80000"
CMD_SET_GAIN_UPPER = "v4l2-ctl -d 0 --set-ctrl=gain_auto_upper_limit=330"

def set_strobe(state):
    cmd = CMD_STRB_ON if state else CMD_STRB_OFF
    ret = ss.Popen(cmd, stdout=ss.PIPE, shell=True).communicate()
    print("strobe:"+str(state))

def show_video_info(v):
    print("width:"+str(v.get(cv.CAP_PROP_FRAME_WIDTH)))
    print("height:"+str(v.get(cv.CAP_PROP_FRAME_HEIGHT)))
    print("fps:"+str(v.get(cv.CAP_PROP_FPS)))
    print("buffer:"+str(v.get(cv.CAP_PROP_BUFFERSIZE)))

def save_image(f):
    t = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = LOG_DIR+t+".jpg"
    cv.putText(f,t,(0,20),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,160,255),1,cv.LINE_AA)
    cv.putText(f,"GAIN:"+str(vid.get(cv.CAP_PROP_GAIN)),(0,40),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,160,255),1,cv.LINE_AA)
    cv.putText(f,"EXP:"+str(vid.get(cv.CAP_PROP_EXPOSURE)),(0,60),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,160,255),1,cv.LINE_AA)
    cv.imwrite(filename, f)
    print("image saved:"+filename)

if not os.path.exists("/dev/video0"):
    print("error: video0 does not exist.")
    time.sleep(2)
    sys.exit()

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid.set(cv.CAP_PROP_BUFFERSIZE, 1)
ret, frame = vid.read()
#show_video_info(vid)

ret = ss.Popen(CMD_SET_EXPOSURE_REF, stdout=ss.PIPE, shell=True).communicate()
ret = ss.Popen(CMD_SET_EXPOSURE_AUTO, shell=True).communicate()
ret = ss.Popen(CMD_SET_GAIN_UPPER, stdout=ss.PIPE, shell=True).communicate()

zoom_x = 0

while True:
    ret, frame = vid.read()

    # ズーム
    if zoom_x:
        frame = cv.resize(frame, dsize=None, fx=ZOOM_REF**zoom_x, fy=ZOOM_REF**zoom_x)
        print(ZOOM_REF**zoom_x)
        height,width = frame.shape[:2]
        posx = int((height - HEIGHT)/2)
        posy = int((width - WIDTH)/2)
        frame = frame[posx:posx+HEIGHT,posy:posy+WIDTH]

    # グリッド追加
    if FLG_GRID:
        frame = cv.line(frame, (int(WIDTH/2),0), (int(WIDTH/2),HEIGHT), LINE_COLOR, thickness=2)
        frame = cv.line(frame, (0,int(HEIGHT/2)), (WIDTH,int(HEIGHT/2)), LINE_COLOR, thickness=2)

    cv.namedWindow("frame", cv.WINDOW_NORMAL)
    cv.imshow('frame', frame)
    print("gain:",vid.get(cv.CAP_PROP_GAIN))
    print("expo:",vid.get(cv.CAP_PROP_EXPOSURE))

    # キー入力別処理
    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('g'):
        FLG_GRID = not FLG_GRID
    elif key == ord('s'):
        FLG_STRB = not FLG_STRB
        set_strobe(FLG_STRB)
    elif key == ord('p'):
        save_image(frame)
        cv.imshow('frame', np.full_like(frame,255))
        cv.waitKey(200)
    elif key == ord(','):
        if zoom_x:
            zoom_x -= 1
    elif key == ord('.'):
        if zoom_x < ZOOM_MAX:
            zoom_x += 1

set_strobe(STRB_OFF)
vid.release()
cv.destroyAllWindows()
