import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import db.connection
from PIL import ImageTk, Image
import os
import frm.utils as utils
import shutil
import cv2

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
        self.title('Gerenciar Estudantes')

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
        self.btnClean = Button(self.frame2, text="Limpar Campos", width=20, command=self.cleanFields).grid(row=1, column=3, columnspan=2, pady=(3), padx=(3, 0))

        #btns
        self.btnSave = Button(self.frame2, text="Salvar", width=10, command=self.on_click_btn_salvar).grid(row=0, column=3, pady=(3), padx=(3, 0))
        self.btnDelete = Button(self.frame2, text="Deletar", width=10, command=self.on_click_btn_delete).grid(row=0, column=4, pady=(3), padx=(3, 0))
        
        #btn Load Image
        self.btnLoad = Button(self.frame2, text="Tirar Foto", width=20, command=self.tirarFoto).grid(row=2, column=0, columnspan=5, pady=(3), padx=(3, 0))

        self.imgFrame = Frame(self.frame2)
        self.imgFrame.grid(row=3, column=0, pady=(3), padx=(3, 0), columnspan=5, rowspan=1 )
        
        self.noImage = "image/no_image.png"
        self.tmpImage = "tmpFoto.png"

        self.imageUrl = self.noImage
        self.img, im = utils.loadImageH(self.imageUrl, maxHeight=240)
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
        self.tree.bind("<<TreeviewSelect>>", self.selectItem)

        #controle para saber se mostra imagem tmpFoto.png ou no_image.png
        self.showTmpImage = False
        self.lastShowTmpImage = False

        self.updateTree()

        self.close_window = False

        self.lastEntrySize = 0
        
        self.updateFoto = False

    def __del__( self ):
        if hasattr( self, "registraFoto" ):
            self.registraFoto.destroy

    def tirarFoto( self ):
        self.updateFoto = True

    def selectItem( self, event ):
        try:
            tree = event.widget
            selection = [self.tree.item(item)["values"] for item in tree.selection()]
            ra = selection[0][0]
            name = selection[0][1]
            self.setEntryText( self.labelRaField, str(ra) )
            self.setEntryText( self.labelNameField, name )
            self.imageUrl = "./image/" + str(ra) + ".png"
            self.changeImage( self.imageUrl )
        except:
            None

    def setEntryText(self, entryTgt, text):
        entryTgt.delete(0,END)
        entryTgt.insert(0,text)

    def closeWindow( self ):
        self.close_window = True

    def changeImage(self, url):
        self.img, image = utils.loadImageH(url, maxHeight=240)
        self.label.config( image=self.img )
        image.save( self.tmpImage )

    def myLoop(self):
        # db_ = db.connection.BancoDeDados()
        # db_.conecta_db()
        # db_.getPresencaBetweenDates( "2022-10-28", "2022-10-31")
        # db_.desconecta_db()

        if( self.showTmpImage != self.lastShowTmpImage ):
            if( self.showTmpImage ):
                self.imageUrl = self.tmpImage
            else:
                self.imageUrl = self.noImage
            
            self.changeImage( self.imageUrl )
        try:
            if( self.lastEntrySize != len( self.labelRaField.get() ) and
                self.labelRaField.get().isdigit ):
                self.lastEntrySize = len( self.labelRaField.get() )
                if( self.lastEntrySize == 7 ):
                    self.db.conecta_db()
                    aluno = self.db.getAlunoByRA( self.labelRaField.get() )
                    if( aluno ):
                        self.setEntryText( self.labelNameField, str(aluno[1]) )
                        self.imageUrl = "./image/" + str(aluno[0]) + ".png"
                        self.changeImage( self.imageUrl )
        except:
            None
                
        self.showTmpImage = False
        self.lastShowTmpImage = self.showTmpImage

    def updateTree( self ):
        self.tree.delete(*self.tree.get_children())
        self.db.conecta_db()
        alunosList = self.db.listarAlunos()
        self.db.desconecta_db()

        for i in alunosList:
            ra = i[0]
            nome = i[1]
            self.tree.insert("",'end',text="L2"+str(i),values=(str(ra),nome))

    def on_click_btn_delete( self ):
        ra = self.labelRaField.get()

        try:
            self.db.excluirAluno(ra)
            os.remove( self.imageUrl )
            self.cleanFields()
            messagebox.showerror("Excluir aluno", "Excluído com sucesso!.")
        except:
            messagebox.showerror("Erro ao excluir", "Erro: RA de aluno não existe.")

        self.updateTree()
        self.lift()

    def on_click_btn_salvar( self ):
        ra = self.labelRaField.get()
        nome = self.labelNameField.get()

        if self.imageUrl == self.noImage:
            messagebox.showerror("Erro foto", "Erro: Não há foto para registrar.")
            return
        elif( ra == "" or nome == "" ):
            messagebox.showerror("Campo Vazio", "Erro: Preencha todos os campos.")
            return
        elif( ra.isdigit() == False ):
            messagebox.showerror("Erro RA", "Erro: O RA deve conter apenas números.")
            return
        elif( len(ra) != 7 ):
             messagebox.showerror('Erro RA', f'Erro: O RA deve conter 7 caracteres e contém {len(ra)}.')
             return
        
        self.db.conecta_db()
        
        src = "tmpFoto.png"
        dst = "./image/" + str(ra) + ".png"

        try:
            self.db.addAluno( int(ra), nome )
            messagebox.showinfo("RA Salvo", "Aluno registrado.")            
            shutil.copy(src, dst)
        except:
            self.db.updateAluno( int(ra), nome )
            messagebox.showinfo("RA Salvo", "Aluno atualizado.")
            shutil.copy(src, dst)

        self.db.desconecta_db()
        self.cleanFields()
        self.updateTree()
        self.lift()
    
    def cleanFields( self ):
        self.setEntryText( self.labelRaField, "" )
        self.setEntryText( self.labelNameField, "" )
        self.changeImage( self.noImage )
        