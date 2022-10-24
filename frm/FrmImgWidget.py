import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import imutils
import cv2
import numpy as np
import mediapipe as mp
import face_recognition as fr
import frm.utils as utils

class VideoWidget( Label ):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.cam = cv2.VideoCapture(0)

    def getFaceRegisterStatus(self):
        if hasattr(self, 'faceStatus'):
            return self.faceStatus
        return 1

    def myLoop(self):
        ret, imgFrame = self.cam.read()
        self.image = imgFrame

        if ret:
            # cv2 uses `BGR` but `GUI` needs `RGB
            frame = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)

            # convert to PIL image
            img = Image.fromarray(frame)

            # convert to Tkinter image
            photo = ImageTk.PhotoImage(image=img)
        
            # solution for bug in `PhotoImage`
            self.photo = photo

            reconhecimento = mp.solutions.face_detection
            reconhecedor = reconhecimento.FaceDetection()
            lista_rostos = reconhecedor.process(imgFrame)
            print( type(lista_rostos.detections) )

            listSize = 0
            if lista_rostos.detections:
                listSize = len(lista_rostos.detections)

            if listSize > 1:
                self.faceStatus = 0
                print( "mais de um rosto" )
            elif listSize == 0:
                self.faceStatus = 1
                print( "nao ha rostos ")
            else:
                self.faceStatus = 2
                print("Sucesso!")

            try:
                if hasattr( self, "configure" ):
                    self.configure( image=self.photo )
            except:
                None

        else:
            self.imageUrl = "image/no_image.png"
            self.photo = utils.loadImageH(self.imageUrl, maxHeight=240)
            self.configure( image = self.photo )




