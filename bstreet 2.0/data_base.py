import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="bigsstreet",
            port=3306
        )

        if conexao.is_connected():
            print("Conectado ao MySQL com sucesso!")
            return conexao

    except Error as e:
        print("ERRO AO CONECTAR AO MYSQL:", e)
        return None