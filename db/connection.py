import os
import sqlite3

class BancoDeDados():


    def conecta_db(self):
        try:

            self.conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
            self.cursor = self.conn.cursor()
            print("conexao estabelecida com sucesso")

            self.sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(self.sqlite_select_Query)
            record = self.cursor.fetchall()
            print("SQLite Database Version is: ", record)
            #self.cursor.close()

        except:
            print("erro ao conectar no banco")

    def desconecta_db(self):
        self.conn.close()

    def createDB(self):
        conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"\\facesDB.sqlite")
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS alunos
                    ( [ra_aluno] INTEGER PRIMARY KEY, [nome_aluno] TEXT )
                ''')

    def addAluno(self, ra, nome):
        self.conn.execute(f"INSERT INTO alunos(ra_aluno, nome_aluno) values('{ra}', '{nome}')")
        try:
            self.conn.commit()
            return True
        except ConnectionAbortedError:
            return False

    def getAlunoByRA( self, ra ):
        self.conn.execute(f"SELECT * FROM alunos WHERE ra_aluno = '{ra}'")
        c = self.conn.cursor()
        return c.fetchone()

    def listarAlunos(self):
        self.conn.execute( f"SELECT * FROM alunos" )
        c = self.conn.cursor()
        return c.fetchall()

    def checkAlunoExists( self, ra ):
        self.conn.execute( f"SELECT EXISTS(SELECT 1 FROM alunos WHERE ra_aluno='{ra}')")
        c = self.conn.cursor()
        if c.fetchone:
            return True
        return False

    def updateAluno( self, ra, nome ):
        self.conn.execute( f"UPDATE alunos SET nome_aluno='{nome}' WHERE ra_aluno='{ra}'" )
        self.conn.commit()

    def excluirAluno(self, ra):
        self.conn.execute( f"DELETE FROM alunos WHERE ra_aluno = {ra}" )
        
        try:
            self.conn.commit()
            return True
        except ConnectionAbortedError:
            return False
        
    

