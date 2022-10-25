import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import frm.utils as utils

import frm.FrmImgWidget as imgWidget
import os

class FmrRegistrarRosto(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

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

        # self.btnTakePhoto = Button(self, text="Tirar Foto", width=10, command=self.doNothing).pack()
        self.btnFoto = Button(self, text="Tirar Foto", width=15, command=self.on_click_btn_foto).pack()

    def myLoop(self):
        self.videoWidget.myLoop()
        faceStatus = self.videoWidget.getFaceRegisterStatus()

        if faceStatus == imgWidget.FaceStatus.ENCONTROU_MAIS_DE_UM_ROSTO:
            self.labelDescrip.config( text="Reconhecendo mais de um rosto",
                                    bg="#8a3d3d",
                                    fg="black" )
        elif faceStatus == imgWidget.FaceStatus.PROCURANDO:
            self.labelDescrip.config( text="Procurando...",
                                    bg="#FDD017",
                                    fg="black" )
        elif faceStatus == imgWidget.FaceStatus.OFF:
            self.labelDescrip.config( text="Camera desligada",
                                    bg="#8a3d3d",
                                    fg="black" )
        elif faceStatus == imgWidget.FaceStatus.ENCONTROU_UM_ROSTO:
            self.labelDescrip.config( text="Reconhecendo rosto",
                                    bg="#1f4a1b",
                                    fg="white")

    def on_click_btn_foto( self ):
        a = 0

    def doNothing():
        a = 0