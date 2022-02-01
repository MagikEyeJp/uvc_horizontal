import cv2 as cv
import numpy as np

FLG_MASK = False

def show_data_array(data):
    print("type: ", type(data))
    print("ndim: ", data.ndim)
    print("shape: ", data.shape)
    print("size: ", data.size)
    print("dtype: ", data.dtype)

vid = cv.VideoCapture(0)
ret, frame = vid.read()

frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = vid.get(cv.CAP_PROP_FPS)
print(frame_width)
print(frame_height)
print(video_fps)

show_data_array(frame)

mask = np.full_like(frame,0)
mask = cv.rectangle(mask, (319,0), (321,480), (0,0,170), thickness=-1)
mask = cv.rectangle(mask, (0,239), (640,241), (0,0,170), thickness=-1)

while True:
    ret, frame = vid.read()
    cv.imshow('frame', (frame^mask) if FLG_MASK else frame )
    print(FLG_MASK)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('m'):
        FLG_MASK = not FLG_MASK

vid.release()
cv.destroyAllWindows()
