from transform import fourPtTrans
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
from auto_canny import auto_canny
import img2pdf


def convert(pic):
    image = cv2.imread(pic)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = auto_canny(gray)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break
    try:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    except:
        return "Cannot Find Contours!! Please send a better image in which the document can be distinguished from the surface!!",0

    warped = fourPtTrans(orig, screenCnt.reshape(4, 2) * ratio)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255
    doc = 'doc.jpg'
    cv2.imwrite(doc, warped)
    return doc,1

def toPdf(image):
	with open("doc.pdf", "wb") as f:
		f.write(img2pdf.convert(image))