import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import frm.utils as utils
from tkinter import messagebox
import frm.FrmImgWidget as imgWidget
import time
import os
import cv2

class FmrRegistrarRosto(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self._start_time = time.time()

        self.geometry('650x550')
        self.maxsize( 650,550 )
        self.title('Registro de rosto')

        self.labelDescrip = Label( self, text="Success", font="Arial 16", fg="white" )
        self.labelDescrip.config(bg="#1f4a1b")
        self.labelDescrip.pack()
        # labelDescrip = Label( self, text="Error!", font="Arial 16", fg="red" )
        # labelDescrip.config(bg="#8a3d3d")

        # os.chdir("..")
        # filePath = os.getcwd() + "/image/no_image.png"
        self.img = utils.loadImageH( 'image/no_image.png', 350 ) #tmp
        # print( filePath )

        self.videoWidget = imgWidget.VideoWidget(self, imgWidget.VideoRole.TAKE_PHOTO_WIDGET)
        self.videoWidget.pack()
        self.videoWidget.setPause( False )

        # self.btnTakePhoto = Button(self, text="Tirar Foto", width=10, command=self.doNothing).pack()
        self.btnFoto = Button(self, text="Tirar Foto", width=15, command=self.on_click_btn_foto).pack()

        self.savedFoto = False

        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.close_window = False

    def closeWindow( self ):
        # self.videoWidget.destroy()
        self.videoWidget.setPause( True )
        self.close_window = True
        

    def myLoop(self):
        now = time.time()
        self.dt = now - self._start_time

        if self.videoWidget:

            self.videoWidget.myLoop()
            self.faceStatus = self.videoWidget.getFaceRegisterStatus()

            try:
                if self.faceStatus == imgWidget.FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO:
                    self.labelDescrip.config( text="Reconhecendo mais de um rosto",
                                            bg="#8a3d3d",
                                            fg="black" )
                elif self.faceStatus == imgWidget.FaceStatus.PROCURANDO:
                    self.labelDescrip.config( text="Procurando...",
                                            bg="#FDD017",
                                            fg="black" )
                elif self.faceStatus == imgWidget.FaceStatus.OFF:
                    self.labelDescrip.config( text="Camera desligada",
                                            bg="#8a3d3d",
                                            fg="black" )
                elif self.faceStatus == imgWidget.FaceStatus.TIRE_FOTO:
                    self.labelDescrip.config( text="Reconhecendo rosto",
                                            bg="#1f4a1b",
                                            fg="white") 
            except:
                None
        
        if self.close_window:
            self.destroy()

    def resetSavedPhoto( self ):
        self.savedFoto = False

    def on_click_btn_foto( self ):
        if self.faceStatus == imgWidget.FaceStatus.TIRE_FOTO:
            videoFrame = self.videoWidget.getVideoFrame()
            
            fileName = "./tmpFoto.png"
            cv2.imwrite(fileName, videoFrame)

            self.savedFoto = True

            self.videoWidget.setPause( True )

            self.destroy()
        elif self.faceStatus == imgWidget.FaceStatus.PROCURANDO:
            messagebox.showerror("Rosto ao tirar foto", "Erro: Rosto não reconhecido.")
        elif self.faceStatus == imgWidget.FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO:
            messagebox.showerror("Rosto ao tirar foto", "Erro: Foi reconhecido mais de um rosto.")
        

    def doNothing():
        a = 0