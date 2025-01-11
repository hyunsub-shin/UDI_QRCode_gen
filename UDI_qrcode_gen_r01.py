from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
# for Add logo
from PIL import Image
from PyQt5.QtWidgets import QFileDialog

import os

## pip install qrcode ##
import qrcode
## pip install pystrich ##
from pystrich.datamatrix import DataMatrixEncoder


####################################################
app = QtWidgets.QApplication([])
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
ui = uic.loadUi(BASE_DIR + r'\UDI_qrcode_gen_r01.ui')
ui.setWindowTitle("UDI Code Generator - made by hsshin")
####################################################


###############
## Variables ##
###############
# init background color 'block'
back_r = 255
back_b = 255
back_g = 255
back_col = QColor(back_r, back_g, back_b)
back_frm = ui.label_back_color
back_frm.setStyleSheet('QWidget {background-color: %s }' % back_col.name())

# init background color 'white'
text_r = 0
text_g = 0
text_b = 0
text_col = QColor(text_r, text_g, text_b)
text_frm = ui.label_text_color
text_frm.setStyleSheet('QWidget {background-color: %s }' % text_col.name())

logo_enable = 0

# default DataMatrix Select
ui.radioButton_DataMatrix.setChecked(True)

# init Disable for DataMatrix
ui.pushButton_back_color.setDisabled(True)
ui.pushButton_text_color.setDisabled(True)
ui.lineEdit_qr_ver.setEnabled(False)
ui.lineEdit_dot_size.setEnabled(False)
ui.lineEdit_border_size.setEnabled(False)
ui.checkBox_logo_enable.setEnabled(False)


def Gen_Code():
    img_size = ui.lineEdit_img_size.text()
    
    GTIN = ui.lineEdit_gtin.text()
    ROT = ui.lineEdit_rot.text()
    DATE = ui.lineEdit_date.text()
    EXPIRATION = ui.lineEdit_expiration.text()
    SERIAL = ui.lineEdit_serial.text()
    S_NO = ui.lineEdit_s_no.text()
    count = int(ui.lineEdit_count.text())
      
    if count == '':
        count = 1
    
    ######################
    ##   QR Code Gen    ##
    ######################
    if (ui.radioButton_QRCode.isChecked()):        
        ver = ui.lineEdit_qr_ver.text()
        dot_size = ui.lineEdit_dot_size.text()
        border_size = ui.lineEdit_border_size.text()
        
        qr = qrcode.QRCode(version=int(ver), 
                       box_size=int(dot_size), 
                       border=int(border_size), 
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
        
        for n in range(count):
            qr.clear()
            
            qr_str = "(01)" + GTIN            
            if ROT != '':
                qr_str = qr_str + "(10)" + ROT
            if DATE != '':
                qr_str = qr_str + "(11)" + DATE
            if EXPIRATION != '':
                qr_str = qr_str + "(17)" + EXPIRATION
            if SERIAL != '':
                qr_str = qr_str + "(21)" + SERIAL
            if S_NO != '':
                NUMBER = str((int(S_NO) + n)).zfill(len(S_NO))
                qr_str = qr_str + "-" + NUMBER
                
            qr.add_data(qr_str)
            
            # Make the QR code
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color=text_col.name(), back_color=back_col.name())
            
            if(logo_enable == True):
                #### Add Logo ####
                # 로고 이미지 열기
                logo = Image.open(sel_logo)
                # 로고 이미지 크기 조정
                logo_size = int(min(img.size) / 4)
                logo = logo.resize((logo_size, logo_size))
                # QR 코드 이미지에 로고 붙이기
                img.paste(logo, box=(int((img.size[0] - logo_size) / 2), int((img.size[1] - logo_size) / 2)))
                ####################
            
            # img resize for UDI label size
            img = img.resize([int(img_size),int(img_size)])
            
            # Save the QR code image
            if S_NO != '':
                file_name = "UDI_" + SERIAL + "-" + NUMBER  + ".png"
            else:
                file_name = "UDI_" + SERIAL + "-" + str(n)  + ".png"
                
            img.save(file_name)
            
    ######################
    ##  DataMatrix Gen  ##
    ######################
    if (ui.radioButton_DataMatrix.isChecked()):        
        for n in range(count):           
            data = "(01)" + GTIN            
            if ROT != '':
                data = data + "(10)" + ROT
            if DATE != '':
                data = data + "(11)" + DATE
            if EXPIRATION != '':
                data = data + "(17)" + EXPIRATION
            if SERIAL != '':
                data = data + "(21)" + SERIAL
            if S_NO != '':
                NUMBER = str((int(S_NO) + n)).zfill(len(S_NO))
                data = data + "-" + NUMBER
                
            encoder = DataMatrixEncoder(data)
            
            if S_NO != '':
                file_name = "UDI_" + SERIAL + "-" + NUMBER  + ".png"
            else:
                file_name = "UDI_" + SERIAL + "-" + str(n)  + ".png"
                
            encoder.save(file_name)
            
            img = Image.open(file_name)
            img = img.resize([int(img_size),int(img_size)])
            img.save(file_name)
                
    # diplay image
    qPixmapVar = QPixmap()
    qPixmapVar.load(file_name)
    
    ui.label_qrcode.setPixmap(qPixmapVar)
    if(int(img_size)>200):
        # resize label size scale 200x200
        ui.label_qrcode.setPixmap(qPixmapVar.scaled(200, 200))


'''
## USE qrcode ##
def Gen_QRCode():
    ver = ui.lineEdit_qr_ver.text()
    dot_size = ui.lineEdit_dot_size.text()
    border_size = ui.lineEdit_border_size.text()
    img_size = ui.lineEdit_img_size.text()
    
    qr = qrcode.QRCode(version=int(ver), 
                       box_size=int(dot_size), 
                       border=int(border_size), 
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    
    GTIN = ui.lineEdit_gtin.text()
    ROT = ui.lineEdit_rot.text()
    SERIAL = ui.lineEdit_serial.text()
    S_NO = ui.lineEdit_s_no.text()
    count = int(ui.lineEdit_count.text())
    # print(count)
    
    for n in range(count):
        qr.clear()
        NUMBER = str((int(S_NO) + n)).zfill(len(S_NO))
        qr.add_data("(01)" + GTIN + "(10)" + ROT + "(21)" + SERIAL + "-" + NUMBER)
        # print(str(S_NO + n).zfill(2))

        # Make the QR code
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color=text_col.name(), back_color=back_col.name())
        
        if(logo_enable == True):
            #### Add Logo ####
            # 로고 이미지 열기
            logo = Image.open(sel_logo)
            # 로고 이미지 크기 조정
            logo_size = int(min(img.size) / 4)
            logo = logo.resize((logo_size, logo_size))
            # QR 코드 이미지에 로고 붙이기
            img.paste(logo, box=(int((img.size[0] - logo_size) / 2), int((img.size[1] - logo_size) / 2)))
            ####################
    
        # img resize for UDI label size
        # img = img.resize((60,60))
        img = img.resize([int(img_size),int(img_size)])
        
        # Save the QR code image
        file_name = "UDI_" + SERIAL + "-" + NUMBER + ".png"
        img.save(file_name)

    # diplay image
    qPixmapVar = QPixmap()
    qPixmapVar.load(file_name)
    
    ui.label_qrcode.setPixmap(qPixmapVar)
    if(int(img_size)>200):
        # resize label size scale 200x200
        ui.label_qrcode.setPixmap(qPixmapVar.scaled(200, 200))

def Gen_DataMatrix():
    img_size = ui.lineEdit_img_size.text()
    
    GTIN = ui.lineEdit_gtin.text()
    ROT = ui.lineEdit_rot.text()
    SERIAL = ui.lineEdit_serial.text()
    S_NO = ui.lineEdit_s_no.text()
    count = int(ui.lineEdit_count.text())    
    
    for n in range(count):
        NUMBER = str((int(S_NO) + n)).zfill(len(S_NO))
        data = "(01)" + GTIN + "(10)" + ROT + "(21)" + SERIAL + "-" + NUMBER
        
        encoder = DataMatrixEncoder(data)
         
        file_name = "UDI_" + SERIAL + "-" + NUMBER + ".png"
        encoder.save(file_name)
        
        img = Image.open(file_name)
        img = img.resize([int(img_size),int(img_size)])
        img.save(file_name)
        
    # diplay image
    qPixmapVar = QPixmap()
    qPixmapVar.load(file_name)
    
    ui.label_qrcode.setPixmap(qPixmapVar)
    if(int(img_size)>200):
        # resize label size scale 200x200
        ui.label_qrcode.setPixmap(qPixmapVar.scaled(200, 200))
'''        
 
 
def SetBackgroundColor():
    global back_col, back_r, back_g, back_b
    back_col = QtWidgets.QColorDialog.getColor()
    
    if back_col.isValid():
        back_frm.setStyleSheet('QWidget { background-color: %s }' % back_col.name())
        
        rgb = back_col.getRgb()
        back_r = rgb[0]
        back_g = rgb[1]
        back_b = rgb[2]


def SetTextColor():
    global text_col, text_r, text_g, text_b
    text_col = QtWidgets.QColorDialog.getColor()
    
    if text_col.isValid():
        text_frm.setStyleSheet('QWidget { background-color: %s }' % text_col.name())
        
        rgb = text_col.getRgb()
        text_r = rgb[0]
        text_g = rgb[1]
        text_b = rgb[2]
        

def input_logo(state):
    global logo_enable, sel_logo
    
    if state == 2:
        logo_enable = 1
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog 
        logo_file, _ = QFileDialog.getOpenFileName(None, "logo", "그림 파일 (*.png *.bmp *.jpg);;모든 파일 (*)", options=options)
        if logo_file:
            print(f"선택한 그림: {logo_file}")
            sel_logo = logo_file
        else:
            ui.checkBox_logo_enable.setCheckState(False)
            logo_enable = 0
    else:
        # ui.checkBox_logo_enable.setCheckState(False)
        logo_enable = 0        


def check_radio_btn():
    if ui.radioButton_QRCode.isChecked():
        ui.pushButton_back_color.setEnabled(True)
        ui.pushButton_text_color.setEnabled(True)
        ui.lineEdit_qr_ver.setEnabled(True)
        ui.lineEdit_dot_size.setEnabled(True)
        ui.lineEdit_border_size.setEnabled(True)
        ui.checkBox_logo_enable.setEnabled(True)    
    elif ui.radioButton_DataMatrix.isChecked():
        ui.pushButton_back_color.setDisabled(True)
        ui.pushButton_text_color.setDisabled(True)
        ui.lineEdit_qr_ver.setEnabled(False)
        ui.lineEdit_dot_size.setEnabled(False)
        ui.lineEdit_border_size.setEnabled(False)
        ui.checkBox_logo_enable.setEnabled(False)


ui.lineEdit_gtin.setPlaceholderText('14자리 숫자')
ui.lineEdit_rot.setPlaceholderText('option')
ui.lineEdit_date.setPlaceholderText('option(yymmdd)')
ui.lineEdit_expiration.setPlaceholderText('option(yymmdd)')
ui.lineEdit_serial.setPlaceholderText('option')
ui.lineEdit_s_no.setPlaceholderText('nnn')
ui.lineEdit_count.setPlaceholderText('생성개수')

ui.radioButton_DataMatrix.clicked.connect(check_radio_btn)
ui.radioButton_QRCode.clicked.connect(check_radio_btn)
ui.pushButton_gen_qr.clicked.connect(Gen_Code)    
ui.pushButton_back_color.clicked.connect(SetBackgroundColor)
ui.pushButton_text_color.clicked.connect(SetTextColor)
ui.checkBox_logo_enable.stateChanged.connect(input_logo)


ui.show()
app.exec()
