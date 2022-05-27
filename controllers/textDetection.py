import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\/tesseract.exe'

class TextDetection():

    def __init__(self, image):
        self.image = image
        self.regions = [[(2033, 0), (492, 186), 'text', 'InvNumber'],
                       [(339, 416), (167, 69), 'text', 'CustNumber']]
        #cv2.imshow('image', self.image)
        w, h, ch = self.image.shape
        self.textFound = []
        #print(w, h)

        self.crop()

    def crop(self):
        for x, r in enumerate(self.regions):
            #print(r[0][1], r[1][1]+r[0][1], r[0][0], r[1][0]+r[0][0])
            cropSections = self.image[r[0][1]:r[1][1]+r[0][1], r[0][0]:r[1][0]+r[0][0]]
            #cv2.imshow(str(x), cropSections)

            if r[2] == 'text':
                textVal = pytesseract.image_to_string(cropSections)
                self.textFound.append(textVal.strip())