import numpy as np
import os

# Class of invoice data
# holds current invoice
# invoiceScans - the cropped and translated image
# displayInvoices - the images that are displayed (lower quality)
# invoice_number - the current invoice numbers
# customer_number - the current customer numbers
# page_numbers - the current page numbers
# file_name - the file name this needs to be saved to
# email - email to be sent to (currently not implemented)
class Invoice():

    def __init__(self):
        self.invoiceScans = []
        self.displayInvoices = []
        self.invoice_number = []
        self.customer_number = []
        self.page_number = []
        self.file_name = ''
        self.email = ''

    # clears all data in invoice
    def clear(self):
        self.invoiceScans.clear()
        self.displayInvoices.clear()
        self.invoice_number.clear()
        self.customer_number.clear()
        self.page_number.clear()
        self.file_name = ''
        self.email = ''

    # adds page to an invoice
    def addPage(self, invNum, custNum, pageNum, invScan, dispInv):
        self.invoiceScans.append(invScan)
        self.displayInvoices.append(dispInv)
        self.invoice_number.append(invNum)
        self.customer_number.append(custNum)
        self.page_number.append(pageNum)
        #print('adding page')

    # currenlty not implemented
    # as of right now a new scan can just be called
    # if you wanted to remove a page a deleted page
    # button would have to be added
    def removePage(self):
        print('removing page')

    # sets the filename
    # saved in folder on desktop
    # this could be changed
    def setFilename(self, filename):
        self.file_name = os.environ['USERPROFILE'] + '\Desktop'
        self.file_name += '\InvoiceImages\\'
        self.file_name += filename
    
    # not implemented right now
    # this would set the email seperately as the email
    # is not currently show on the invoice itself
    def setEmail(self):
        print('setting email')

    # used in testing
    # prints the invoice data to console
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