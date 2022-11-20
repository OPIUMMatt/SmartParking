import sqlite3  
from sqlite3 import Error
import os


pastaApp = os.path.dirname(__file__)
nomeBanco = pastaApp + "//bd//patio.db"

def ConexaoBanco():
    con = None
    
    try:
        con = sqlite3.connect(nomeBanco)
    except Error as ex:
        print(ex)

    return con

def dql(query): #select
    vcon = ConexaoBanco()
    c = vcon.cursor()
    c.execute(query)
    res = c.fetchall()
    vcon.close()
    return res

def dml(query): #insert, update, delete
    try:
        vcon = ConexaoBanco()
        c = vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    except Error as ex:
        print(ex)