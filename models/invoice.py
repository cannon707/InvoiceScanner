import numpy as np
import os

class Invoice():

    def __init__(self):
        self.invoiceScans = []
        self.displayInvoices = []
        self.invoice_number = []
        self.customer_number = []
        self.page_number = []
        self.file_name = ''
        self.email = ''

    def clear(self):
        self.invoiceScans.clear()
        self.displayInvoices.clear()
        self.invoice_number.clear()
        self.customer_number.clear()
        self.page_number.clear()
        self.file_name = ''
        self.email = ''

    def addPage(self, invNum, custNum, pageNum, invScan, dispInv):
        self.invoiceScans.append(invScan)
        self.displayInvoices.append(dispInv)
        self.invoice_number.append(invNum)
        self.customer_number.append(custNum)
        self.page_number.append(pageNum)
        #print('adding page')

    def removePage(self):
        print('removing page')

    def getValues(self):
        print('getting invoice values')

    def setFilename(self, filename):
        self.file_name = os.environ['USERPROFILE'] + '\Desktop'
        self.file_name += '\InvoiceImages\\'
        self.file_name += filename
    
    def setEmail(self):
        print('setting email')

    def printInvoiceData(self):
        #for i in range(len(self.invoiceScans)):
        #    cv2.imshow(str(i), self.invoiceScans[i])
        print('Printing Invoice Data')
        print(self.invoice_number)
        print()
        print(self.customer_number)
        print()
        print(self.page_number)
        print()