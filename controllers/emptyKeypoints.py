
# This file was left in although this method do not work with
# the current invoices
# depending on whats being scanned this may be a better way
import cv2

class EmptyKey():
    def __init__(self):
        self.keypoints = None
        self.emptyDest = None
        self.getEmpty()

    def getEmpty(self):
        empty = cv2.imread('assets/emptyInvoice.jpg')
        orb = cv2.ORB_create(5000)
        self.keypoints, self.emptyDest = orb.detectAndCompute(empty, None)
        #testEmpty = cv2.drawKeypoints(empty, self.keypoints, None)
        #cv2.imshow('testEmpty', testEmpty)
