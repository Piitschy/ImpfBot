import pytesseract
import numpy as np
import cv2
import string

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

#erosion
def erode(image):
    kernel = np.ones((2,2),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
whitelist = string.ascii_lowercase+(''.join(str(e) for e in range(0,10)))

def read(img):
    image = cv2.imread(img)
    (h, w) = image.shape[:2]
    image_size = h*w
    bottom = image[h-2:h, 0:w]
    mean = cv2.mean(bottom)[0]
    bordersize = 10
    image = cv2.copyMakeBorder(
        image,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )
    mser = cv2.MSER_create()
    mser.setMaxArea(int(image_size/2))
    mser.setMinArea(50)
    image = get_grayscale(image)
    image= thresholding(image)
    image = erode(image)
    image= dilate(image)
    image= thresholding(image)
    image = erode(image)
    regions, rects = mser.detectRegions(image)
    rects = sorted(rects,key=lambda x: int(x[0]))
    # With the rects you can e.g. crop the letters
    word = ""
    for (x, y, w, h) in rects:
        letter = image[y-2:y+h+2,x-2:x+w+2]
        word+=pytesseract.image_to_string(letter,lang="deu", config='--psm 10 --oem 3 -c tessedit_char_whitelist='+whitelist)

    return word.replace("","").replace("\n","")

