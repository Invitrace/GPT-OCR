import cv2

def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def preprocess_img(img):
    # ..Ignore other preprocess function right now..
    gray = get_grayscale(img)
    return gray
