from multiprocessing import connection
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
import time

class VideoRole( Enum ):
    TAKE_PHOTO_WIDGET = 0
    RECOGNIZE_PERSON = 1

class FaceStatus( Enum ):
    OFF = -1 #
    ENCONTROU_MAIS_DE_UM_ROSTO = 0 #
    PROCURANDO = 1 #
    TIRE_FOTO = 2 #
    MATCH_FOTO = 3
    ACHOU = 4
    
class Aluno():
    ra_aluno = 0
    nome_aluno = ""

class VideoWidget( Label ):
    
    def __init__(self, parent, role):
        super().__init__(parent)

        self._alunoRertorno = Aluno()

        self.last_face_status = FaceStatus.PROCURANDO

        self.db = db.connection.BancoDeDados()

        self.role = role

        self.cam = cv2.VideoCapture(0)

        self.getImageSets()

        self.times_to_detect = []

        self.paused = False

        self.dt = 0
        self.last_time = time.time()
        self.time_now = time.time()

        self.match_time_show = 0

    def getAlunoFound(self):
        return self._alunoRertorno
    
    def __del__( self ):
        print( "Cam release ")
        self.cam.release()

    def getFaceRegisterStatus(self):
        if hasattr(self, 'faceStatus'):
            return self.faceStatus
        return FaceStatus.OFF

    def setPause( self, isPaused ):
        self.paused = isPaused

    def setRole( self, newRole: VideoRole ):
        self.role = newRole

    def myLoop(self):
        self.time_now = time.time()
        self.dt = self.time_now - self.last_time
        self.last_time = self.time_now
        
        if self.paused == True:
            return False

        ret, imgFrame = self.cam.read()
        
        if ret:
            videoFrame = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(videoFrame)

            img2 = img.convert("RGB")
            self.image = imgFrame
            self.videoFrameRGB = imgFrame
           
            if self.role == VideoRole.TAKE_PHOTO_WIDGET:
                # convert to PIL image
                self.times_to_detect = []

                # convert to Tkinter image
                photo = ImageTk.PhotoImage(image=img)
            
                # # solution for bug in `PhotoImage`
                self.photo = photo

                self.faceStatus = FaceStatus.TIRE_FOTO

                try:
                    if hasattr( self, "configure" ):
                        self.configure( image=self.photo )
                except:
                    None
            elif self.role == VideoRole.RECOGNIZE_PERSON:

                img2 = np.array(img2)
                img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)

                # convert to Tkinter image
                photo = ImageTk.PhotoImage(image=img)
            
                # solution for bug in `PhotoImage`
                self.photo = photo

                try:
                    if hasattr( self, "configure" ):
                        self.configure( image=self.photo )
                except:
                    None

                # if img2:
                    
                
                try:
                    self.encodeVideo = fr.face_encodings( img2, model = "large" )
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

                    elif len(self.encodeVideo) > 1 :
                        self.faceStatus = FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO
                        self.times_to_detect = []
                    elif len(self.encodeVideo) == 0:
                        self.faceStatus = FaceStatus.PROCURANDO
                        self.times_to_detect = []

                    if( self.faceStatus == FaceStatus.ACHOU ):
                        self.times_to_detect.append(1)
                    
                    if( len(self.times_to_detect) >= 5 ):
                        if len(self.times_to_detect) == 5 :
                            ownDB = db.connection.BancoDeDados()
                            ownDB.conecta_db()
                            ownDB.addPresenca(self.alunosToCompare[i][0])
                            ownDB.desconecta_db()
                        self.faceStatus = FaceStatus.MATCH_FOTO
                        if( len(self.alunosToCompare) == 0 ): 
                            return
                        self._alunoRertorno.ra_aluno = self.alunosToCompare[i][0]
                        self._alunoRertorno.nome_aluno = self.alunosToCompare[i][1]
                except:
                    self.faceStatus = FaceStatus.PROCURANDO
                    self.times_to_detect = []
                
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
            try:
                fromImg = fr.load_image_file( "./image/" + str(aluno[0]) + ".png" )
                encodeFrom = fr.face_encodings(fromImg, model = "small")[0]
                self.encodeList.append(encodeFrom)
            except:
                None

    def getVideoFrame( self ):
        try:
            return self.videoFrameRGB
        except:
            return None
