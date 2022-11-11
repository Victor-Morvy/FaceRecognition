import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import frm.utils as utils
import datetime
import re
import calendar
from tkcalendar import Calendar, DateEntry
import db.connection as connection
import pandas as pd
import tkinter.filedialog
import openpyxl

class FrmRelatorio( tk.Toplevel ):
    def __init__(self, parent):
        super().__init__(parent)

        self.month = datetime.datetime.now().month

        y = 635
        self.geometry('1024x' + str(y))
        self.maxsize( 1024, y )
        self.minsize( 1024, y)
        self.title('Relatório de Presença')

        self.labelJump2 = Label(self, text="Escola a data:")
        self.labelJump2.pack()

        self.findFrame = Frame(self, bd=3)
        self.findFrame.pack(fill=X)

        # create a combobox
        self.selected_month = tk.StringVar()
        self.selected_month.trace('w',self.on_field_change)
        self.month_cb = ttk.Combobox(self.findFrame, textvariable=self.selected_month)

        db = connection.BancoDeDados()
        db.conecta_db()
        dateLists = db.getListOfDates()
        db.desconecta_db()

        self.month_cb['values']=( dateLists )
        self.month_cb['state'] = 'readonly'
        self.month_cb.pack()

        self.btn_print = ttk.Button(self.findFrame, text="Gerar Excel", command=self.toExcel).pack()

        self.treeResults = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"), show='headings', height=28 )
        self.treeResults.column("# 1", anchor=CENTER)
        self.treeResults.heading("# 1", text="")
        self.treeResults.column("# 2", anchor=CENTER)
        self.treeResults.heading("# 2", text="")
        self.treeResults.column("# 3", anchor=CENTER)
        self.treeResults.heading("# 3", text="")
        self.treeResults.column("# 4", anchor=CENTER)
        self.treeResults.heading("# 4", text="")
        self.treeResults.column("# 5", anchor=CENTER)
        self.treeResults.heading("# 5", text="")
        self.treeResults.column("# 6", anchor=CENTER)
        self.treeResults.heading("# 6", text="")
        self.treeResults.column("# 7", anchor=CENTER)
        self.treeResults.heading("# 7", text="")
        self.treeResults.column("# 8", anchor=CENTER)
        self.treeResults.heading("# 8", text="")
        self.treeResults.column("# 9", anchor=CENTER)
        self.treeResults.heading("# 9", text="")
        self.treeResults.column("# 10", anchor=CENTER)
        self.treeResults.heading("# 10", text="")
        
        self.vsby = ttk.Scrollbar(self, orient="vertical", command=self.treeResults.yview)
        self.vsb = ttk.Scrollbar(self, orient="horizontal", command=self.treeResults.xview)
        self.vsb.place( y=615, width=1022)
        self.vsby.place( x=1008, y=45, width=18, height=570)

        self.treeResults.configure(xscrollcommand=self.vsb.set, yscrollcommand=self.vsby.set)

        self.treeResults.pack( fill='x' )

        self.treeResults.configure(columns=("c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"))
        
        self.treeResults.column("# 3", anchor=CENTER)
        self.treeResults.heading("# 3", text="")

        self.reloadTable()

    def toExcel(self):
        self.xmlContent = pd.DataFrame( self.data_tables, index=self.index_tables, columns=self.columns_tables )
        
        savePath = tkinter.filedialog.asksaveasfile( mode="w", defaultextension=".xlsx", filetypes=[("Excel File", ".xlsx")])
        if( savePath is None):
            return

        savePath = savePath.name

        print( "SavePath " + savePath )
            
        self.xmlContent.to_excel(savePath)


    def on_field_change(self, index, value, op):
        self.reloadTable()
        

    def reloadTable( self ):
        columns, days, alunos = self.generateTableData()

        cols = ["c0"]

        i = 1
        for day in days:
            cols.append( "c" + str(i))
            i += 1
        
        self.treeResults.configure(columns=cols)
        
        columWidth = 75
        self.treeResults.column("# " + str( 1 ), anchor='nw', width=columWidth, stretch=False)
        i = 2

        self.columns_tables = []
        self.index_tables = []
        self.data_tables = []

        # self.columns_tables.append("")
        for day in days:
            self.treeResults.column("# " + str( i ), anchor='nw', width=columWidth, stretch=False)
            anoMesDia = day[1].split('-')
            patternDay = anoMesDia[2] + "/" + anoMesDia[1] + "/" + anoMesDia[0]
            self.columns_tables.append(patternDay)
            self.treeResults.heading("# "+ str( i ), text=patternDay)

            i += 1

        i = 0

        try:
            self.treeResults.delete(*self.treeResults.get_children())
        except:
            None
        
        alunoVec = []
        for aluno in alunos:
            alunoVec.append( aluno[0] )
            self.index_tables.append( aluno[ 0 ] )

            for day in days:
                if day[0] == aluno[0]:
                    alunoVec.append( "presente" )
                else:
                    alunoVec.append( "faltou" )
            
            self.treeResults.insert("",'end',text="L"+str(i),values=alunoVec)
            i += 1
            alunoVec.pop(0)
            self.data_tables.append(alunoVec)
            alunoVec = []

    def generateTableData( self ):
        selected = self.selected_month.get()
        if len(selected) == 0:
            return (), (), ()
        month = selected.split('-')[1]
        year = selected.split('-')[0]
        lastDay = calendar.monthrange( int( year ), int( month ) )[1]
        dateFrom = year + "-" + month + "-" + "01"
        dateTo = year + "-" + month + "-" + str( lastDay )

        db = connection.BancoDeDados()
        db.conecta_db()
        dateLists = db.getPresencaBetweenDates( dateFrom, dateTo )
        daysList = db.getDaysOfMonth( dateFrom, dateTo )
        alunos = db.getAlunosByDays( dateFrom, dateTo )
        db.desconecta_db()
        
        return dateLists, daysList, alunos

    def createCBValues( self ):

        db = connection.BancoDeDados()
        db.conecta_db()
        dateLists = db.getListOfDates()
        db.desconecta_db()

        self.month_cb['values']=( dateLists )

    def validateDate( self, input ):
        format = "%Y-%m-%d"
        res = False
        try:
            res = bool(datetime.datetime.strptime(input, format))
        except ValueError:
            res = False
        return res

    def myLoop( self ):
        a = 0

    def openCalendar( self, event ):
        def print_sel():
            print(cal.selection_get())

        top = tk.Toplevel(self)

        cal = Calendar(top,
                    font="Arial 14", selectmode='day',
                    cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()
        
        