import connection

db = connection.BancoDeDados()

db.conecta_db()
# db.createDBTableAlunos()
db.createDBTablePresenca()
# db.cleanDB()
db.desconecta_db()
