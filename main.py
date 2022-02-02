import cv2 as cv
import numpy as np
import subprocess as ss

FLG_MASK = False
FLG_STRB = False
COLOR = (0,0,255)
#WIDTH = 1440
#HEIGHT = 1080
WIDTH = 640
HEIGHT = 480

CMD_STRB_ON = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=1"
CMD_STRB_OFF = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=0"

def set_strobe(state):
    cmd = CMD_STRB_ON if state else CMD_STRB_OFF
    ret = ss.Popen(cmd, stdout=ss.PIPE, shell=True).communicate()
    print(cmd)

def show_data_array(data):
    print("type: ", type(data))
    print("ndim: ", data.ndim)
    print("shape: ", data.shape)
    print("size: ", data.size)
    print("dtype: ", data.dtype)

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid.set(cv.CAP_PROP_BUFFERSIZE, 1)
ret, frame = vid.read()

frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = vid.get(cv.CAP_PROP_FPS)
buffer = vid.get(cv.CAP_PROP_BUFFERSIZE)
print(frame_width)
print(frame_height)
print(video_fps)
print(buffer)

show_data_array(frame)

while True:
    ret, frame = vid.read()

    if FLG_MASK:
        frame = cv.line(frame, (int(WIDTH/2),0), (int(WIDTH/2),HEIGHT), COLOR, thickness=2)
        frame = cv.line(frame, (0,int(HEIGHT/2)), (WIDTH,int(HEIGHT/2)), COLOR, thickness=2)
    cv.imshow('frame', frame)
#    cv.imshow('frame', (frame^mask) if FLG_MASK else frame )
#    print(FLG_MASK)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('m'):
        FLG_MASK = not FLG_MASK
    elif key == ord('s'):
        FLG_STRB = not FLG_STRB
        set_strobe(FLG_STRB)

vid.release()
cv.destroyAllWindows()
