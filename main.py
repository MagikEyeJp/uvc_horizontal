import cv2 as cv
import numpy as np

FLG_MASK = False
WIDTH = 1440
HEIGHT = 1080
#WIDTH = 640
#HEIGHT = 480

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

mask = np.full_like(frame,0)
mask = cv.line(mask, (int(WIDTH/2),0), (int(WIDTH/2),HEIGHT), (0,0,170), thickness=2)
mask = cv.line(mask, (0,int(HEIGHT/2)), (WIDTH,int(HEIGHT/2)), (0,0,170), thickness=2)


while True:
    ret, frame = vid.read()
    cv.imshow('frame', (frame^mask) if FLG_MASK else frame )
#    print(FLG_MASK)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('m'):
        FLG_MASK = not FLG_MASK

vid.release()
cv.destroyAllWindows()
