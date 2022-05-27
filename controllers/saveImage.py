from PIL import Image
import PIL
import cv2
import models.invoice as inv
import numpy as np

class saveImage():
    def __init__(self, invoice: inv.Invoice):
        self.invoice = invoice
        self.canSave = False
        self.appendImages()
        self.saveToFile()

    def appendImages(self):   
        self.imageList = []
        for scan in self.invoice.invoiceScans:
            self.canSave = True
            scan = cv2.cvtColor(scan, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(scan)
            self.imageList.append(image_pil)
            #imageList.append(cv2.hconcat(image))
        #self.final_image = cv2.vconcat(imageList)
        

    def saveToFile(self):
        print(self.invoice.file_name)
        if self.canSave:
            print('here')
            self.imageList[0].save(self.invoice.file_name, save_all=True, append_images=self.imageList[1:])
            #cv2.imwrite(self.invoice.file_name, self.final_image)
    
    
