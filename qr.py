import pyqrcode
def generateqr(s):
    qr = pyqrcode.create(s)
    qr.png(s+'.png',scale = 8)