import connection

db = connection.BancoDeDados()

db.conecta_db()
db.createDBTableAlunos()
db.createDBTablePresenca()
# db.cleanDB()
# db.addPresenca( 1200146, "2022-11-11")
# db.addPresenca( 1200146, "2022-11-12")
# db.addPresenca( 1200146, "2022-11-13")
# db.addPresenca( 1200146, "2022-11-14")
# db.addPresenca( 1200146, "2022-11-15")
# db.addPresenca( 1200146, "2022-11-16")
# db.addPresenca( 1200146, "2022-11-17")
# db.addPresenca( 1200146, "2022-11-18")
# db.addPresenca( 1200146, "2022-11-19")
# db.addPresenca( 1200146, "2022-11-20")
db.desconecta_db()
