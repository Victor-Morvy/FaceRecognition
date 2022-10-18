import tkinter as tk
from tkinter import *
from tkinter import ttk


class FrmAdmin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('800x600')
        self.title('Toplevel Window')

        # self.columnconfigure( 0, weight = 300 )

        # create RA label
        self.ra = Label(self, text="RA")
        self.ra.grid(row=0, column=0, pady=(3), padx=(3, 0))
        self.ra_field = Entry(self)    
        self.ra_field.grid(row=0, column=1, ipadx="100")

        # create a Name label
        self.name = Label(self, text="Name" )
        self.name.grid(row=1, column=0, pady=(3), padx=(3, 0))
        self.name_field = Entry(self)
        self.name_field.grid(row=1, column=1, ipadx="100")

        #btns
        self.btnSearch = Button(self, text="Search", width=10, command=self.fecha_janela).grid(row=0, column=2, pady=(3), padx=(6, 0))
        self.btnSave = Button(self, text="Save", width=10, command=self.fecha_janela).grid(row=0, column=3, pady=(3), padx=(3, 0))
        self.btnDelete = Button(self, text="Delete", width=10, command=self.fecha_janela).grid(row=0, column=4, pady=(3), padx=(3, 0))
        
        # create Image Label
        self.imageUrl = ""
        self.image = Label(self, text="No Image" )
        self.image.grid(row=3, column=0, pady=(3), padx=(3, 0), rowspan=2, columnspan=2)
        self.image.config(bg="gray")

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)

    def fecha_janela():
        a = 0