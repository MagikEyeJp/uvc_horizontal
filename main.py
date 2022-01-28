import cv2 as cv
import numpy as np

def show_data_array(data):
    print("type: ", type(data))
    print("ndim: ", data.ndim)
    print("shape: ", data.shape)
    print("size: ", data.size)
    print("dtype: ", data.dtype)

vid = cv.VideoCapture(0)
ret, frame = vid.read()

# image size or you can get this from image shape
frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = vid.get(cv.CAP_PROP_FPS)
print(frame_width)
print(frame_height)
print(video_fps)

show_data_array(frame)

mask = np.full_like(frame,255)
mask = cv.rectangle(mask, (319,0), (321,480), (0,0,255), thickness=-1)
mask = cv.rectangle(mask, (0,239), (640,241), (0,0,255), thickness=-1)

while True:
    ret, frame = vid.read()
#    cv.imshow('frame', frame)
    cv.imshow('frame', cv.bitwise_and(frame,mask))
#    cv.imshow('frame', cv.addWeighted(src1=frame,alpha=0.8,src2=mask,beta=0.2,gamma=0))
#    cv.imshow('frame', frame+mask)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()