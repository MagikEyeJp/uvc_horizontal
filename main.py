import cv2 as cv
import subprocess as ss
import sys
import os

FLG_MASK = False
FLG_STRB = False
LINE_COLOR = (0,0,255)
WIDTH = 640
HEIGHT = 480

CMD_STRB_ON = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=1"
CMD_STRB_OFF = "v4l2-ctl -d 0 --set-ctrl=strobe_enable=0"

def set_strobe(state):
    cmd = CMD_STRB_ON if state else CMD_STRB_OFF
    ret = ss.Popen(cmd, stdout=ss.PIPE, shell=True).communicate()
    print("strobe:"+str(state))

def show_video_info(v):
    print("width:"+str(vid.get(cv.CAP_PROP_FRAME_WIDTH)))
    print("height:"+str(vid.get(cv.CAP_PROP_FRAME_HEIGHT)))
    print("fps:"+str(vid.get(cv.CAP_PROP_FPS)))
    print("buffer:"+str(vid.get(cv.CAP_PROP_BUFFERSIZE)))

if not os.path.exists("/dev/video0"):
    print("error: video0 does not exist.")
    sys.exit()

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid.set(cv.CAP_PROP_BUFFERSIZE, 1)
#show_video_info(vid)

while True:
    ret, frame = vid.read()

    # グリッド追加
    if FLG_MASK:
        frame = cv.line(frame, (int(WIDTH/2),0), (int(WIDTH/2),HEIGHT), LINE_COLOR, thickness=2)
        frame = cv.line(frame, (0,int(HEIGHT/2)), (WIDTH,int(HEIGHT/2)), LINE_COLOR, thickness=2)
    cv.imshow('frame', frame)

    # キー入力別処理
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
