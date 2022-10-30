import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import db.connection
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
    TIRE_FOTO = 2
    MATCH_FOTO = 3
    ACHOU = 4
    
class VideoWidget( Label ):
    
    def __init__(self, parent, role):
        super().__init__(parent)

        self.last_face_status = FaceStatus.PROCURANDO

        self.db = db.connection.BancoDeDados()

        self.role = role

        self.cam = cv2.VideoCapture(0)

        self.getImageSets()

        self.times_to_detect = []

        self.paused = False
    
    def __del__( self ):
        print( "Cam release ")
        self.cam.release()

    def getFaceRegisterStatus(self):
        if hasattr(self, 'faceStatus'):
            return self.faceStatus
        return FaceStatus.OFF

    def setPause( self, isPaused ):
        # if hasattr(self, "cam"):
        #     self.cam.release()
        self.paused = isPaused

    def setRole( self, newRole: VideoRole ):
        self.role = newRole

    def myLoop(self):
        if self.paused == True:
            # self.cam.release()
            # self.photo = None
            return False

        ret, imgFrame = self.cam.read()

        # cv2 uses `BGR` but `GUI` needs `RGB
        
        if ret:
            videoFrame = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(videoFrame)
            
            img2 = img.convert("RGB")
            self.image = imgFrame
            self.videoFrameRGB = imgFrame
            img2 = np.array(img2)
            img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
            if self.role == VideoRole.TAKE_PHOTO_WIDGET:
                # convert to PIL image
                

                # convert to Tkinter image
                photo = ImageTk.PhotoImage(image=img)
            
                # # solution for bug in `PhotoImage`
                self.photo = photo

                self.faceStatus = FaceStatus.TIRE_FOTO


                # reconhecimento = mp.solutions.face_detection
                # reconhecedor = reconhecimento.FaceDetection()
                # lista_rostos = reconhecedor.process(imgFrame)

                # listSize = 0
                # if lista_rostos.detections:
                #     listSize = len(lista_rostos.detections)

                # if listSize > 1:
                #     self.faceStatus = FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO
                # elif listSize == 0:
                #     self.faceStatus = FaceStatus.PROCURANDO
                # else:
                #     self.faceStatus = FaceStatus.TIRE_FOTO


                try:
                    if hasattr( self, "configure" ):
                        self.configure( image=self.photo )
                except:
                    None
            elif self.role == VideoRole.RECOGNIZE_PERSON:

                # print( "videoFrame type " + str( type(self.image) ))
                # convert to Tkinter image
                photo = ImageTk.PhotoImage(image=img)
            
                # solution for bug in `PhotoImage`
                self.photo = photo

                try:
                    if hasattr( self, "configure" ):
                        self.configure( image=self.photo )
                except:
                    None

                self.encodeVideo = fr.face_encodings( img2, model = "large" )

                self.faceStatus = FaceStatus.PROCURANDO

                if( self.last_face_status != self.faceStatus ):
                    self.times_to_detect = []
                
                i = 0
                if len(self.encodeVideo) == 1 :
                    
                    hold = False
                    achou = fr.compare_faces(self.encodeList, self.encodeVideo[0])
                    for item in achou:
                        if item:
                            hold = True
                            break
                        i += 1

                    if hold:
                        self.faceStatus = FaceStatus.ACHOU
                        # print( "RA ALUNO " + str( self.alunosToCompare[i][0] ) )
                elif len(self.encodeVideo) > 1 :
                    self.faceStatus = FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO
                elif len(self.encodeVideo) == 0:
                    self.faceStatus = FaceStatus.PROCURANDO

                

                if( self.faceStatus == FaceStatus.ACHOU and len(self.times_to_detect) < 5 ):
                    self.times_to_detect.append(1)

                if( len(self.times_to_detect) == 5 ):
                    self.faceStatus = FaceStatus.MATCH_FOTO
                    print( "Achou " + str( self.alunosToCompare[i][0] ) + " " + self.alunosToCompare[i][1])


                # cv2.rectangle(videoFrame, (faceloc[3],faceloc[0]),
                #                         (faceloc[1],faceloc[2]),
                #                         (0,255,0),2 )
                



        else:
            self.imageUrl = "image/no_image.png"
            self.photo = utils.loadImageH(self.imageUrl, maxHeight=240)
            self.configure( image = self.photo )


    #atualizara as tuplas do banco de dados dos alunos para comparação com a imagem da camera atual
    #update: também fará o face_encoding para tentar acelerar o processo
    def getImageSets( self ):
        self.db.conecta_db()
        self.alunosToCompare = self.db.listarAlunos()
        
        self.encodeList = []

        for aluno in self.alunosToCompare:
            fromImg = fr.load_image_file( "./image/" + str(aluno[0]) + ".png" )
            encodeFrom = fr.face_encodings(fromImg, model = "large")[0]
            self.encodeList.append(encodeFrom)

    def getVideoFrame( self ):
        try:
            return self.videoFrameRGB
        except:
            return None
