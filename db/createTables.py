import connection

db = connection.BancoDeDados()

db.conecta_db()
db.createDB()
# db.cleanDB()
db.desconecta_db()
