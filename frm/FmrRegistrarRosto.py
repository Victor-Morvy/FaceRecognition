import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import frm.utils as utils
import os

class FmrRegistrarRosto(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('650x450')
        self.maxsize( 650,450 )
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


        self.labelJump2 = Label(self, text="GERENCIAR CADASTRO")
        self.labelJump2.pack()

        self.label = Label(self, image = self.img)
        self.label.pack()

        self.btnTakePhoto = Button(self, text="Tirar Foto", width=10, command=self.doNothing).pack()

    def doNothing():
        a = 0