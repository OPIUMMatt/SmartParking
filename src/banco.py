#Esse arquivo guarda as funções que serão executadas para fazer a comunicação do app com o banco de dados

#Importando dependencias
import sqlite3  
from sqlite3 import Error
import os

#Pegando o caminho do app
pastaApp = os.path.dirname(__file__)

#Setando o caminho do arquivo do banco de dados
nomeBanco = pastaApp + "//bd//patio.db"

#### FUNÇÕES

#Função de conexão com o banco
def ConexaoBanco():
    #Iniciando a variável de comunicação
    con = None
    
    #Tentando comunicar com o banco de dados, se não conseguir printa o erro
    try:
        con = sqlite3.connect(nomeBanco)
    except Error as ex:
        print(ex)

    #Retornando a conexão
    return con

#Método dql para usar o select
def dql(query): 

    #Iniciando conexão com o banco
    vcon = ConexaoBanco()

    #Configurando o cursor
    c = vcon.cursor()

    #Executando query
    c.execute(query)

    #Pegando resposta do banco de dados
    res = c.fetchall()

    #Fechando conexão
    vcon.close()

    #Retornando a resposta
    return res

#Método dml para usar o insert, update, delete
def dml(query):

    #Tenta fazer a query, se não der printa o erro
    try:
        #Iniciando conexão
        vcon = ConexaoBanco()

        #Configurando o cursor
        c = vcon.cursor()

        #Executando query
        c.execute(query)

        #Dando commit na query
        vcon.commit()

        #Fechando conexão
        vcon.close()

    except Error as ex:
        print(ex)