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
        self.month_cb = ttk.Combobox(self, textvariable=self.selected_month)

        db = connection.BancoDeDados()
        db.conecta_db()
        dateLists = db.getListOfDates()
        db.desconecta_db()

        self.month_cb['values']=( dateLists )
        # prevent typing a value
        self.month_cb['state'] = 'readonly'
        # self.month_cb.grid( row=1, column=1 )
        self.month_cb.pack()

        self.treeResults = ttk.Treeview(self, column=("c1", "c2"), show='headings', height=28 )
        self.treeResults.column("# 1", anchor=CENTER)
        self.treeResults.heading("# 1", text="RA")
        self.treeResults.column("# 2", anchor=CENTER)
        self.treeResults.heading("# 2", text="Name")

        self.treeResults.pack()

        self.treeResults.configure(columns=("c2", "c3", "c4"))
        
        self.treeResults.column("# 3", anchor=CENTER)
        self.treeResults.heading("# 3", text="Name")

        self.reloadTable()

        # # create DESDE label
        # self.dataFrom = Label(self.findFrame, text="Desde (AAAA-mm-dd):")
        # self.dataFrom.grid(row=0, column=0, pady=(3), padx=(3, 0))
        # self.dataFromField = Entry(self.findFrame)    
        # self.dataFromField.grid(row=0, column=1, ipadx="5")
        # # self.dataFromField.bind("<1>", self.openCalendar())
        
        # # create ATE label
        # self.dataAte = Label(self.findFrame, text="Até (AAAA-mm-dd):" )
        # self.dataAte.grid(row=0, column=2, pady=(3), padx=(3, 0))
        # self.dataAteField = Entry(self.findFrame)
        # self.dataAteField.grid(row=0, column=3, ipadx="5")
 
        # self.btnClean = Button(self.findFrame, text="Procurar", width=20, command=self.procurarData)
        # self.btnClean.grid(row=0, column=4, columnspan=2, pady=(3), padx=(3, 0))
    def on_field_change(self, index, value, op):
        # print (f"combobox updated to {value}")
        self.reloadTable()
        

    def reloadTable( self ):
        columns, days, alunos = self.generateTableData()

        cols = ["c0"]

        i = 1
        for day in days:
            cols.append( "c" + str(i))
            i += 1
        
        self.treeResults.configure(columns=cols)
        
        i = 2
        for day in days:
            self.treeResults.column("# " + str( i ), anchor=CENTER)
            self.treeResults.heading("# "+ str( i ), text=day[1])
            i += 1

        i = 0

        try:
            self.treeResults.delete(*self.treeResults.get_children())
        except:
            None

        alunoVec = []
        for aluno in alunos:
            alunoVec.append( aluno[0] )

            for day in days:
                if day[0] == aluno[0]:
                    alunoVec.append( "presente" )
                else:
                    alunoVec.append( "faltou" )
            
            self.treeResults.insert("",'end',text="L"+str(i),values=alunoVec)
            i += 1
            alunoVec = []


    def generateTableData( self ):
        selected = self.selected_month.get()
        if len(selected) == 0:
            return ()
        print( "Blue " + str(len(selected) ) )
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

    def procurarData( self ):
        a = 0
        validateFrom = self.validateDate( self.dataFromField.get() )
        validateAte = self.validateDate( self.dataAteField.get() )
        print( "validateFrom " + str(validateFrom) + " validateAte " + str(validateAte) )

    def validateDate( self, input ):
        datePattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
        format = "%Y-%m-%d"
        res = False
        try:
            res = bool(datetime.datetime.strptime(input, format))
        except ValueError:
            res = False
        # ret = re.search( datePattern, input )
        # print (ret.group())
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
        
        