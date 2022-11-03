import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image


class FrmSobre( tk.Toplevel ):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('550x350')
        self.maxsize( 550, 350 )
        self.minsize( 550, 350)
        self.title('Sobre...')

        self.window_label = Label( self, text="""
        Trabalho de Conclusão de Curso\n
        \n
        Sistema de registro de chamada por reconhecimento facial\n
        \n
        Alunos:\n
        RA 2004526 – Victor Hugo Martins de Oliveira\n
        RA 1902879 - Paula Akemi Tanaka\n
        RA 1800935 – Luiz Almeida\n
        \n
        \n
        
        """ )

        self.window_label.pack()