from tkinter import *
from PIL import ImageTk, Image
import datetime

def timeNowToStr( self, data ):
    now = datetime.datetime.now()
    return timeNowToStr( now )

def timeToStr( self, data ):
    return data.strftime('%Y/%m/%d')
    
def strToTime( self, strTime):
    return datetime.datetime.strptime(strTime, '%Y/%m/%d')

def loadImage( file, maxWidth = -1 ):
    image = Image.open(file)
    newHeight = image.height
    newWidth = image.width

    finalWidth = -1

    if( maxWidth == -1 ):
        finalWidth = 600
    else:
        finalWidth = maxWidth

    if( image.width > finalWidth ):
        tmpPercent = finalWidth / image.width
        newWidth = finalWidth
        newHeight = tmpPercent * newHeight

    image = image.resize((newWidth, int(newHeight)))
    img = ImageTk.PhotoImage(image)
    return img


def loadImageH( file, maxHeight = -1 ):
    image = Image.open(file)
    newHeight = image.height
    newWidth = image.width

    finalHeight = -1

    if( maxHeight == -1 ):
        finalHeight = 600
    else:
        finalHeight = maxHeight

    if( image.height > finalHeight ):
        tmpPercent = finalHeight / image.height
        newHeight = finalHeight
        newWidth = tmpPercent * newWidth

    image = image.resize((int(newWidth), int(newHeight)))
    img = ImageTk.PhotoImage(image)

    
    return img, image
