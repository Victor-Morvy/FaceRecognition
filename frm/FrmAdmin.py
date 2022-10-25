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

        # make the top right close button minimize (iconify) the main window
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

        self.parent = parent

        self.geometry('550x750')
        self.maxsize( 550, 750 )
        self.minsize( 550, 750)
        self.title('Manage Students')

        self.frame4 = Frame(self, bd=3, relief=SUNKEN, height=10).pack(fill=X)

        self.labelJump2 = Label(self, text="GERENCIAR CADASTRO")
        self.labelJump2.pack()

        self.frame2 = Frame(self, bd=3)
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
        self.btnSave = Button(self.frame2, text="Save", width=10, command=self.on_click_btn_salvar).grid(row=0, column=3, pady=(3), padx=(3, 0))
        self.btnDelete = Button(self.frame2, text="Delete", width=10, command=self.on_click_btn_delete).grid(row=0, column=4, pady=(3), padx=(3, 0))
        
        #btn Load Image
        self.btnLoad = Button(self.frame2, text="Registrar Rosto", width=20, command=self.openRegistraRosto).grid(row=2, column=0, columnspan=5, pady=(3), padx=(3, 0))

        self.imgFrame = Frame(self.frame2)
        self.imgFrame.grid(row=3, column=0, pady=(3), padx=(3, 0), columnspan=5, rowspan=1 )

        self.imageUrl = "image/no_image.png"
        self.img = utils.loadImageH(self.imageUrl, maxHeight=240)
        self.label = Label(self.imgFrame, image = self.img)
        self.label.pack()

        self.frame3 = Frame(self, bd=3, relief=SUNKEN, height=10)
        self.frame3.pack(fill=X)
      
        self.labelJump = Label(self, text="ESTUDANTES CADASTRADOS")
        self.labelJump.pack()
        
        self.frame = Frame(self, bd=3)
        self.frame.pack(fill=X)

        # Add a Treeview widget
        self.tree = ttk.Treeview(self.frame, column=("c1", "c2"), show='headings', height=15)

        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="RA")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Name")

        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.place(x=200+255, y=3, height=200+222 - 105)

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack()

        self.updateTree()

    def closeWindow( self ):
        self.destroy()

    def openRegistraRosto(self):
        self.registraFoto = frmFace.FmrRegistrarRosto( self )  
        self.registraFoto.grab_set()

    def myLoop(self):
        if hasattr( self, "registraFoto"):
            self.registraFoto.myLoop()

        
    def updateTree( self ):
        self.tree.delete(*self.tree.get_children())
        self.db.conecta_db()
        alunosList = self.db.listarAlunos()
        self.db.desconecta_db()

        # print( "len tree " + str(len(alunosList)) )

        for i in alunosList:
            ra = i[0]
            nome = i[1]
            self.tree.insert("",'end',text="L2"+str(i),values=(str(ra),nome))


    

    # def on_click_btn_procurar(self):
    #     ra = self.labelRaField.get()
    #     nome = self.labelNameField.get()

    def on_click_btn_delete( self ):
        ra = self.labelRaField.get()
        try:
            self.db.excluirAluno(ra)
            messagebox.showerror("Excluir aluno", "Excluído com sucesso!.")
        except:
            messagebox.showerror("Erro ao excluir", "Erro: RA de aluno não existe.")

        self.updateTree()


    def on_click_btn_salvar( self ):
        ra = self.labelRaField.get()
        nome = self.labelNameField.get()

        if( ra == "" or nome == "" ):
            messagebox.showerror("Campo Vazio", "Erro: Preencha todos os campos.")
            return

        if( ra.isdigit() == False ):
            messagebox.showerror("Erro RA", "Erro: O RA deve conter apenas números.")
            return

        if( len(ra) != 7 ):
             messagebox.showerror('Erro RA', f'Erro: O RA deve conter 7 caracteres e contém {len(ra)}.')
             return

        #TODO : check if have an image before register
        
        self.db.conecta_db()
        # if( alunoExists ):
        try:
            self.db.addAluno( int(ra), nome )
            messagebox.showinfo("RA Salvo", "Aluno registrado.")
        except:
            self.db.updateAluno( int(ra), nome )
            messagebox.showinfo("RA Salvo", "Aluno atualizado.")

        
        self.db.desconecta_db()

        self.updateTree()
        