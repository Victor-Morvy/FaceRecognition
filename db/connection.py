import os
import sqlite3
# import datetime
from datetime import datetime
# import frm.utils

class BancoDeDados():

    def conecta_db(self):
        try:
            self.conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
            self.cursor = self.conn.cursor()
        except:
            print("erro ao conectar no banco")

    def desconecta_db(self):
        self.conn.close()

    def createDBTablePresenca(self):
        conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS presenca
                    ( [ra_aluno] INTEGER, [data_presenca] TEXT )
                ''')

    def createDBTableAlunos(self):
        conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS alunos
                    ( [ra_aluno] INTEGER PRIMARY KEY, [nome_aluno] TEXT )
                ''')
    
    def cleanDB(self):
        conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
        c = conn.cursor()
        c.execute("DELETE * FROM alunos")

    def addAluno(self, ra, nome):
        self.conn.execute(f"INSERT INTO alunos(ra_aluno, nome_aluno) values('{ra}', '{nome}')")
        try:
            self.conn.commit()
            return True
        except ConnectionAbortedError:
            return False

    def getListOfDates( self ):
        # """
        # WHERE strftime('%s', data_presenca) BETWEEN strftime('%s', '{fromDate}') AND strftime('%s', '{toDate}' )
        #     GROUP BY data_presenca, ra_aluno
        # """
        # """
        # SELECT strftime('%Y-%m-%d','now')
        # WHERE strftime('%s', data_presenca) 
        # BETWEEN strftime('%s', '{fromDate}') AND strftime('%s', '{toDate}' )
        # """
        res = self.conn.execute( f"""
            SELECT strftime("%Y-%m", data_presenca) as 'month-year' 
            from presenca
            group by strftime("%Y-%m", data_presenca)
        """ )
        alunos = res.fetchall()
        return alunos

    def getAlunoByRA( self, ra ):
        self.conecta_db()
        c = self.conn.execute(f"SELECT * FROM alunos WHERE ra_aluno = '{ra}'")
        aluno = c.fetchone()
        self.desconecta_db()
        return aluno

    def listarAlunos(self):
        res = self.conn.execute( f"SELECT * FROM alunos ORDER BY ra_aluno DESC" )
        alunos = res.fetchall()
        return alunos

    def checkAlunoExists( self, ra ):
        self.conecta_db()

        self.conn.execute( f"SELECT EXISTS(SELECT * FROM alunos WHERE ra_aluno='{ra}')")
        c = self.conn.cursor()
        obj = c.fetchone
        if obj:
            self.desconecta_db()
            return True
        self.desconecta_db()
        return False

    def updateAluno( self, ra, nome ):
        self.conecta_db()
        self.conn.execute( f"UPDATE alunos SET nome_aluno='{nome}' WHERE ra_aluno='{ra}'" )
        self.conn.commit()
        self.desconecta_db()

    def excluirAluno(self, ra):
        self.conecta_db()
        self.conn.execute( f"DELETE FROM alunos WHERE ra_aluno = {ra}" )
        
        try:
            self.conn.commit()
            self.desconecta_db()
            return True
        except ConnectionAbortedError:
            self.desconecta_db()
            return False
    
    def getPresencaBetweenDates( self, fromDate, toDate ):
        res = self.conn.execute(f"""
            SELECT * FROM presenca 
            WHERE strftime('%s', data_presenca) BETWEEN strftime('%s', '{fromDate}') AND strftime('%s', '{toDate}' )
            GROUP BY data_presenca, ra_aluno
        """)
        # print( res.fetchall() )
        return res.fetchall()

    def addPresenca( self, ra ) :
        dateNow = datetime.today().strftime('%Y-%m-%d')
        self.conn.execute(f"INSERT INTO presenca(ra_aluno, data_presenca) values('{ra}', '{dateNow}')")
        try:
            self.conn.commit()
            return True
        except ConnectionAbortedError:
            return False