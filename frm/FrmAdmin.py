import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

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
    return img

class FrmAdmin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('650x900')
        self.title('Manage Students')

        # self.columnconfigure( 0, weight = 300 )
        self.frame4 = Frame(self, bd=3, relief=SUNKEN, height=10).pack(fill=X)

        self.labelJump2 = Label(self, text="GERENCIAR CADASTRO")
        self.labelJump2.pack()

        self.frame2 = Frame(self, bd=3)
        # self.frame2.grid(row=0, column=0, columnspan=5, rowspan=5)
        self.frame2.pack(fill=X)

        # create RA label
        self.labelRa = Label(self.frame2, text="RA")
        self.labelRa.grid(row=0, column=0, pady=(3), padx=(3, 0))
        self.labelRaField = Entry(self.frame2)    
        self.labelRaField.grid(row=0, column=1, ipadx="100")

        # create a Name label
        self.labelName = Label(self.frame2, text="Nome" )
        self.labelName.grid(row=1, column=0, pady=(3), padx=(3, 0))
        self.labelNameField = Entry(self.frame2)
        self.labelNameField.grid(row=1, column=1, ipadx="100")

        #btns
        self.btnSearch = Button(self.frame2, text="Search", width=10, command=self.fecha_janela).grid(row=0, column=2, pady=(3), padx=(6, 0))
        self.btnSave = Button(self.frame2, text="Save", width=10, command=self.fecha_janela).grid(row=0, column=3, pady=(3), padx=(3, 0))
        self.btnDelete = Button(self.frame2, text="Delete", width=10, command=self.fecha_janela).grid(row=0, column=4, pady=(3), padx=(3, 0))
        
        #btn Load Image
        self.btnLoad = Button(self.frame2, text="Load Image", width=10, command=self.fecha_janela).grid(row=2, column=0, columnspan=5, pady=(3), padx=(3, 0))

        self.imgFrame = Frame(self.frame2)
        self.imgFrame.grid(row=3, column=0, pady=(3), padx=(3, 0), columnspan=5, rowspan=1 )

        self.imageUrl = "victor1.jpg"
        self.img = loadImageH(self.imageUrl, maxHeight=240)
        self.label = Label(self.imgFrame, image = self.img)
        self.label.pack()
        # create Image Label
        
        # self.labelImage = Label(self.imgFrame, text="No Image\naisjdaisd\naisdjaisd" )
        # self.labelImage.pack()
        # self.labelImage.config(bg="gray")

#/////////////////////////////////////////////////////////////:        

        self.frame3 = Frame(self, bd=3, relief=SUNKEN, height=10)
        # self.frame.grid(row=6, column=1, columnspan=5, rowspan=5)
        self.frame3.pack(fill=X)

#/////////////////////////////////////////////////////////////:        
        self.labelJump = Label(self, text="ESTUDANTES CADASTRADOS")
        self.labelJump.pack()
        
        self.frame = Frame(self, bd=3)
        # self.frame.grid(row=6, column=1, columnspan=5, rowspan=5)
        self.frame.pack(fill=X)

        

        # Add a Treeview widget
        self.tree = ttk.Treeview(self.frame, column=("c1", "c2"), show='headings', height=5)

        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="RA")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Name")

        # Insert the data in Treeview widget
        self.tree.insert('', 'end', text="1", values=('56456561', 'Joe'))
        self.tree.insert('', 'end', text="2", values=('655162', 'Emily'))
        self.tree.insert('', 'end', text="3", values=('3654654564', 'Estilla'))
        self.tree.insert('', 'end', text="4", values=('461561515', 'Percy'))
        self.tree.insert('', 'end', text="5", values=('655655', 'Stephan'))

        self.tree.pack()
        


    def fecha_janela():
        a = 0