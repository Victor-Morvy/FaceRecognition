import connection

db = connection.BancoDeDados()

db.conecta_db()
db.createDBTableAlunos()
# db.cleanDB()
db.desconecta_db()
