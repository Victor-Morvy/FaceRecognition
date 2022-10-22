import connection

db = connection.BancoDeDados()

db.conecta_db()
db.createDB()
db.desconecta_db()
