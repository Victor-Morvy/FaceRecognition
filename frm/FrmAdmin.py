import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import db.connection
from PIL import ImageTk, Image
import frm.utils as utils
import frm.FmrRegistrarRosto as frmFace

class FrmAdmin(tk.Toplevel):

    

    def __init__(self, parent):
        super().__init__(parent)

        self.db = db.connection.BancoDeDados()

        self.parent = parent

        self.geometry('550x850')
        self.maxsize( 550,850 )
        self.minsize( 550, 850)
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
        # self.btnSearch = Button(self.frame2, text="Search", width=10, command=self.on_click_btn_procurar).grid(row=0, column=2, pady=(3), padx=(6, 0))
        self.btnSave = Button(self.frame2, text="Save", width=10, command=self.on_click_btn_salvar).grid(row=0, column=3, pady=(3), padx=(3, 0))
        self.btnDelete = Button(self.frame2, text="Delete", width=10, command=self.fecha_janela).grid(row=0, column=4, pady=(3), padx=(3, 0))
        
        #btn Load Image
        self.btnLoad = Button(self.frame2, text="Registrar Rosto", width=20, command=self.openRegistraRosto).grid(row=2, column=0, columnspan=5, pady=(3), padx=(3, 0))

        self.imgFrame = Frame(self.frame2)
        self.imgFrame.grid(row=3, column=0, pady=(3), padx=(3, 0), columnspan=5, rowspan=1 )

        self.imageUrl = "image/no_image.png"
        self.img = utils.loadImageH(self.imageUrl, maxHeight=240)
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
        self.tree = ttk.Treeview(self.frame, column=("c1", "c2"), show='headings', height=15)

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

        self.tree.insert("",'end',text="L1",values=("Big1","Best"))
        self.tree.insert("",'end',text="L2",values=("Big2","Best"))
        self.tree.insert("",'end',text="L3",values=("Big3","Best"))
        self.tree.insert("",'end',text="L4",values=("Big4","Best"))
        self.tree.insert("",'end',text="L5",values=("Big5","Best"))
        self.tree.insert("",'end',text="L6",values=("Big6","Best"))
        self.tree.insert("",'end',text="L7",values=("Big7","Best"))
        self.tree.insert("",'end',text="L8",values=("Big8","Best"))
        self.tree.insert("",'end',text="L9",values=("Big9","Best"))
        self.tree.insert("",'end',text="L10",values=("Big10","Best"))
        self.tree.insert("",'end',text="L11",values=("Big11","Best"))
        self.tree.insert("",'end',text="L12",values=("Big12","Best"))

        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.place(x=200+255, y=3, height=200+222 - 105)
        # vsb.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack()
        
        # self.registraFoto = frmFace.FmrRegistrarRosto( self )   
            

    def openRegistraRosto(self):
        self.registraFoto = frmFace.FmrRegistrarRosto( self )  
        self.registraFoto.grab_set()

    # def on_click_btn_procurar(self):
    #     ra = self.labelRaField.get()
    #     nome = self.labelNameField.get()

    def on_click_btn_salvar( self ):
        ra = self.labelRaField.get()
        nome = self.labelNameField.get()

        if( ra == "" or nome == "" ):
            messagebox.showerror("Campo Vazio", "Erro: Preencha todos os campos.")
            return
        
        if( ra.count != 7 ):
            messagebox.showerror("RA errado", "Erro: O RA deve conter 7 caracteres.")
            return

        if( ra.isdigit == False ):
            messagebox.showerror("Erro RA", "Erro: O RA deve conter apenas números.")
            return

        #TODO : check if have an image before register
        return

        alunoExists = self.db.checkAlunoExists(ra)

        if( alunoExists ):
            self.db.updateAluno( ra, nome )
        else:
            self.db.addAluno( ra, nome )
        
        messagebox.showinfo("RA Salvo", "Mensagem: Os dados foram salvos.")

        

    def fecha_janela():
        a = 0