import cv2
import numpy as np

class ProccessImage():
    
    def __init__(self, frame):
        self.empty = cv2.imread('assets/emptyInvoice.jpg')
        self.height, self.width, channel = self.empty.shape
        self.firstFrame = frame
        self.editedFrame = frame
        self.frameKeypoints = None
        self.frameDest = None
        self.passed = False
        self.invoiceWarped = None


        #self.getKeypoints()
        #self.match()
        #self.findSimilar()

        # this is the current way it transforms the image
        # by getting the max sized rectangle
        # the method commented out does a different type of transformation
        # that doesn't work as consitently
        self.gray()
        self.canny()
        self.edges = self.findEdges()
        if len(self.edges) == 4:
            self.passed = True
            self.invoice = self.transform()
        else:
            self.invoice = self.empty
            self.passed = False

    #convert image to grayscale
    def gray(self):
        grayFrame = cv2.cvtColor(self.firstFrame, cv2.COLOR_BGR2GRAY)
        self.editedFrame = grayFrame

    #gaussian blur and canny to get edges
    def canny(self):
        gaussian = cv2.GaussianBlur(self.editedFrame, (5,5), 0)
        cannyFrame = cv2.Canny(gaussian, 0, 50)
        self.editedFrame = cannyFrame


    def findEdges(self):
        maxArea = 0
        page = []
        contour, _ = cv2.findContours(self.editedFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        edgeFrame = self.editedFrame.copy()
        edgeFrame = cv2.drawContours(edgeFrame, contour, -1, (255, 0, 255), 4)
        edgeFrame = edgeFrame.copy()
        #cv2.imshow('contour', edgeFrame)
        #cv2.waitKey(0)
        for i in contour:
            area = cv2.contourArea(i)
            if area > 500:
                peri = cv2.arcLength(i, True)
                edges = cv2.approxPolyDP(i, 0.02*peri, True)
                if area > maxArea and len(edges) == 4:
                    page = edges
                    maxArea = area
        if len(page) != 0:
            edgeFrame = cv2.drawContours(self.editedFrame, page, -1, (255, 0, 255), 25)
        return page

    
    def transform(self):
        # https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
        newEdges = self.orderPoints()
        (tl, tr, br, bl) = newEdges

        #widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        #widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        #maxWidth = max(int(widthA), int(widthB))
        maxWidth = self.width
        #heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        #heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        #maxHeight = max(int(heightA), int(heightB))
        maxHeight = self.height

        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]
            ]
            , dtype = "float32")

        transform = cv2.getPerspectiveTransform(newEdges, dst)
        warped = cv2.warpPerspective(self.firstFrame, transform, (maxWidth, maxHeight))
        #cv2.imshow('warped', warped)
        #cv2.waitKey(0)
        #print()
        self.invoiceWarped = warped
        return warped
        
    def orderPoints(self):
        newFrame = np.zeros((4, 2), dtype = "float32")
        sumEdges = []

        # CV2 uses this ordering of points when doing transformations
        #   newFrame[0]         newFrame[1]
        #     *-----------------*
        #     |                 |
        #     |                 |
        #     |                 |
        #     |                 |
        #     |                 |
        #     *-----------------*
        #   newFrame[3]         newFrame[2]
        
        #print('Type: {0}'.format(type(self.edges)))   
        tempEdges = self.edges.sum(axis = 1)

        # min in sum is top left
        # max in sum is bottom right
        sumEdges = tempEdges.sum(axis = 1)
        newFrame[0] = self.edges[np.argmin(sumEdges)]
        newFrame[2] = self.edges[np.argmax(sumEdges)]
        
        #min in diff is top right
        #max in diff is bottom left
        diffEdges = np.diff(tempEdges, axis=1)
        newFrame[1] = self.edges[np.argmin(diffEdges)]
        newFrame[3] = self.edges[np.argmax(diffEdges)]

        return newFrame