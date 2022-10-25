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
from enum import Enum

class VideoRole( Enum ):
    TAKE_PHOTO_WIDGET = 0
    RECOGNIZE_PERSON = 1

class FaceStatus( Enum ):
    OFF = -1
    ENCONTROU_MAIS_DE_UM_ROSTO = 0
    PROCURANDO = 1
    ENCONTROU_UM_ROSTO = 2
    
class VideoWidget( Label ):
    
    def __init__(self, parent, role):
        super().__init__(parent)

        self.role = role

        self.setPause( False )

        self.cam = cv2.VideoCapture(0)

    def getFaceRegisterStatus(self):
        if hasattr(self, 'faceStatus'):
            return self.faceStatus
        return FaceStatus.OFF

    def setPause( self, isPaused ):
        self.paused = isPaused

    def myLoop(self):
        if self.paused == True:
            return

        ret, imgFrame = self.cam.read()

        # cv2 uses `BGR` but `GUI` needs `RGB
        videoFrame = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)
        if ret:
            self.image = imgFrame
            self.videoFrameRGB = videoFrame
            if self.role == VideoRole.TAKE_PHOTO_WIDGET:
                # convert to PIL image
                img = Image.fromarray(videoFrame)

                # convert to Tkinter image
                photo = ImageTk.PhotoImage(image=img)
            
                # solution for bug in `PhotoImage`
                self.photo = photo

                reconhecimento = mp.solutions.face_detection
                reconhecedor = reconhecimento.FaceDetection()
                lista_rostos = reconhecedor.process(imgFrame)

                listSize = 0
                if lista_rostos.detections:
                    listSize = len(lista_rostos.detections)

                if listSize > 1:
                    self.faceStatus = FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO
                elif listSize == 0:
                    self.faceStatus = FaceStatus.PROCURANDO
                else:
                    self.faceStatus = FaceStatus.ENCONTROU_UM_ROSTO

                try:
                    if hasattr( self, "configure" ):
                        self.configure( image=self.photo )
                except:
                    None

        else:
            self.imageUrl = "image/no_image.png"
            self.photo = utils.loadImageH(self.imageUrl, maxHeight=240)
            self.configure( image = self.photo )


    def getVideoFrame( self ):
        try:
            return self.videoFrameRGB
        except:
            return None
