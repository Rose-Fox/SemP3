import cv2 as cv
from time import time
from src import SaveSystem as ss
from src import pre_processing as pp
from src import segmentation as seg

mouse_x, mouse_y = 0, 0


def cropper(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_x, mouse_y = x, y
    if event == cv.EVENT_LBUTTONUP:
        ss.save(param[mouse_y: y, mouse_x:x], ss.SAVE_CROP)


def image_cropper(im):
    image = im
    if type(image) == str:
        image = cv.imread(image)
    cv.imshow("Image", image)
    cv.setMouseCallback("Image", cropper, image)
    cv.waitKey()
    print("crop saved")

def live_feed_capture():
    capture = cv.VideoCapture(0)
    frame_name = "CameraFeed"
    kernels = [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49]
    last_cap = time()
    ret, frame = capture.read()
    cv.imshow(frame_name, frame)

    # Pre-processing Trackers
    cv.createTrackbar("hue lower", frame_name, 0, 360, lambda x: x)
    cv.createTrackbar("hue upper", frame_name, 35, 360, lambda x: x)

    cv.createTrackbar("sat lower", frame_name, 40, 255, lambda x: x)
    cv.createTrackbar("sat upper", frame_name, 255, 255, lambda x: x)

    cv.createTrackbar("val lower", frame_name, 45, 255, lambda x: x)
    cv.createTrackbar("val upper", frame_name, 255, 255, lambda x: x)

    cv.createTrackbar("Closing count", frame_name, 20, 40, lambda x: x)

    # Segmentation Trackers
    cv.createTrackbar("type variable info here", frame_name, 1, 10, lambda x: x)

    while cv.getWindowProperty(frame_name, cv.WND_PROP_VISIBLE) != 0:
        frame_time = time()
        ret, frame = capture.read()
        frame_masked = pp.pre_process(frame, frame_name)
        segmented_image = seg.segmentation(frame_masked, frame_name)
        cv.imshow(frame_name, segmented_image)
        key = cv.waitKey(1) & 0xFF
        if  key == ord('q'):
            break
        if key == ord('c'):
            if frame_time - last_cap > 1:
                ss.save(frame, ss.SAVE_VIDEOCAP)
                last_cap = time()
        if key == ord('g'):
            if frame_time - last_cap > 1:
                ss.save(cv.cvtColor(frame,cv.COLOR_BGR2GRAY), ss.SAVE_VIDEOCAP)
                last_cap = time()
    capture.release()
    cv.destroyAllWindows()

