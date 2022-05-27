from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QIntValidator, QFont, QIcon, QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSlot
import numpy as np
import controllers.camera as cm
import controllers.emptyKeypoints as bc
import controllers.processImage as procI
import controllers.emptyKeypoints as ek
import controllers.textDetection as td
import controllers.saveImage as si
import models.invoice as inv

import cv2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #set up window
        self.resize(300, 300)
        self.setWindowTitle("Invoice Scanner")
        self.setWindowIcon(QIcon("icon.png"))

        #set up empty invoice image | get key
        self.emptyInvoice = QPixmap('assets/emptyInvoice.jpg').scaledToHeight(480, Qt.TransformationMode.FastTransformation)
        self.invoiceImage = QLabel()
        self.invoiceImage.setPixmap(self.emptyInvoice)
        self.currentPage = 0

        #setup layout and invoice model    
        self.mainLayout = QVBoxLayout()
        self.invoice = inv.Invoice()
        self.actionBar()
        self.dataBar()
        self.imageBar()
        self.setLayout(self.mainLayout)

    #top bar that has buttons to do actions
    def actionBar(self):
        actionLayout = QHBoxLayout()

        self.newScanButton = QPushButton("New Scan")
        self.newScanButton.clicked.connect(self.newScan)
        actionLayout.addWidget(self.newScanButton)

        self.addPageButton = QPushButton("Add Page")
        self.addPageButton.clicked.connect(self.addPage)
        actionLayout.addWidget(self.addPageButton)
        
        self.rescanButton = QPushButton("Rescan")
        self.rescanButton.clicked.connect(self.rescan)
        actionLayout.addWidget(self.rescanButton)

        self.saveButton = QPushButton("Save Invoice")
        self.saveButton.clicked.connect(self.writeInvoice)
        actionLayout.addWidget(self.saveButton)

        # Email client could be integrated but LES can use as is
        # right now. So the email options are commented out.

        #self.emailButton = QPushButton("Save and Email")
        #actionLayout.addWidget(self.emailButton)

        self.mainLayout.addLayout(actionLayout)

    # data forms below buttons
    # forms auto filled when invoice scanned
    def dataBar(self):
        dataLayout = QFormLayout()

        # invoice number
        self.invoiceForm = QLineEdit()
        self.invoiceForm.setValidator(QIntValidator())
        self.invoiceForm.setMaxLength(10)
        self.invoiceForm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.invoiceForm.setFont(QFont("Arial",18))
        invLayout = QHBoxLayout()
        invLayout.addWidget(self.invoiceForm)

        # customer number
        self.customerForm = QLineEdit()
        self.customerForm.setValidator(QIntValidator())
        self.customerForm.setMaxLength(8)
        self.customerForm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.customerForm.setFont(QFont("Arial",18))
        customerLayout = QHBoxLayout()
        customerLayout.addWidget(self.customerForm)

        # page number
        self.pageForm = QLineEdit()
        self.pageForm.setValidator(QIntValidator())
        self.pageForm.setMaxLength(4)
        self.pageForm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.pageForm.setFont(QFont("Arial",18))
        self.pageForm.setText(str(self.currentPage))
        pageLayout = QHBoxLayout()
        pageLayout.addWidget(self.pageForm)

        # file name
        self.fileNameForm = QLineEdit()
        self.fileNameForm.setMaxLength(1000)
        self.fileNameForm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fileNameForm.setFont(QFont("Arial",18))
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.fileNameForm)

        # email name
        # self.emailForm = QLineEdit()
        # self.emailForm.setMaxLength(400)
        # self.emailForm.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.emailForm.setFont(QFont("Arial",18))
        # emailLayout = QHBoxLayout()
        # emailLayout.addWidget(self.emailForm)

        #add layouts to main layout
        dataLayout.addRow("Invoice Number", invLayout)
        dataLayout.addRow("Customer Number", customerLayout)
        dataLayout.addRow("Page Number", pageLayout)
        dataLayout.addRow("File Name", fileLayout)
        #dataLayout.addRow("Email", emailLayout)
        self.mainLayout.addLayout(dataLayout)

    # shows video feed and recently scanned invoice
    def imageBar(self):
        cam_width = 640
        cam_height = 480
        self.cameraLabel = QLabel()
        self.cameraLabel.resize(cam_width, cam_height)
        self.video()

        titleLayout = QHBoxLayout()
        camLabel = QLabel("Camera")
        camLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scanLabel = QLabel("Scanned Invoice")
        scanLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLayout.addWidget(camLabel)
        titleLayout.addWidget(scanLabel)

        camScanLayout = QHBoxLayout()
        camScanLayout.addWidget(self.cameraLabel)
        camScanLayout.addWidget(self.invoiceImage)

        imageBarLayout = QVBoxLayout()
        imageBarLayout.addLayout(titleLayout)
        imageBarLayout.addLayout(camScanLayout)

        self.mainLayout.addLayout(imageBarLayout)

    def video(self):
        self.videoThread = cm.Camera()

        self.videoThread.pixmap_signal.connect(self.updateVideoLabel)

        self.videoThread.start()

    def stopVideo(self, event):
        self.videoThread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def updateVideoLabel(self, frame):
        self.frame = frame
        convertedFrame = self.videoThread.convertFrame(frame)
        
        self.cameraLabel.setPixmap(convertedFrame)

    def convertFrame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        line = channel * width
        qt_frame = QImage(rgb_frame.data, width, height, line, QImage.Format.Format_RGB888)
        scaled_frame = qt_frame.scaledToHeight(480, Qt.TransformationMode.FastTransformation)
        return QPixmap.fromImage(scaled_frame)

    def newScan(self):
        self.currentPage = 0
        self.invoice.clear() 
        self.scan()
        self.setDisplayInvoice()

    def addPage(self):
        self.savePage()
        self.scan()
        self.setDisplayInvoice()

    def scan(self):
        self.invoiceScan, self.dispInvoice, passed = self.process()
        if passed:
            TextDetect = td.TextDetection(self.invoiceScan)
            self.invoiceForm.setText(TextDetect.textFound[0])
            self.customerForm.setText(TextDetect.textFound[1])
            self.currentPage += 1
            self.pageForm.setText(str(self.currentPage))
            invoiceFileName = TextDetect.textFound[0] + '.pdf'
            self.fileNameForm.setText(invoiceFileName)

    def setDisplayInvoice(self):
        self.newInvoicePixMap = QPixmap(self.dispInvoice).scaledToHeight(480, Qt.TransformationMode.FastTransformation)
        self.invoiceImage.setPixmap(self.newInvoicePixMap)

    def process(self):
        np = procI.ProccessImage(self.frame)
        passed = np.passed
        scanned = None
        if np.passed:
            scanned = self.convertFrame(np.invoiceWarped)
        return np.invoiceWarped, scanned, passed

    def savePage(self):
        invNum = self.invoiceForm.text()
        custNumber = self.customerForm.text()
        pageNumber = self.currentPage
        self.invoice.addPage(invNum, custNumber, pageNumber, self.invoiceScan, self.dispInvoice)

    def rescan(self):
        self.invoiceScan, self.dispInvoice, passed = self.process()
        if passed:
            TextDetect = td.TextDetection(self.invoiceScan)
            self.invoiceForm.setText(TextDetect.textFound[0])
            self.customerForm.setText(TextDetect.textFound[1])
            self.pageForm.setText(str(self.currentPage))
            invoiceFileName = TextDetect.textFound[0] + '.pdf'
            self.fileNameForm.setText(invoiceFileName)

    def writeInvoice(self):
        filename = self.fileNameForm.text()
        self.invoice.setFilename(filename)
        self.savePage()
        si.saveImage(self.invoice)
        dialog = QMessageBox(parent=self, text='Invoice Saved')
        dialog.setWindowTitle("Save Dialog")
        ret = dialog.exec()

        #self.invoice.printInvoiceData()

    def emailAndWrite(self):
        email = self.emailForm.text()
        self.invoice.setEmail(email)
        self.writeInvoice()
