from credentials import *
import pyodbc
import pandas as pd
import sys


def query_dtts_list(corporativo, query):
    try:
        server, user, pwd, db_name = getConn(corporativo)
        conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db_name+';UID='+user+';PWD='+ pwd
        conn = pyodbc.connect(conn_string)
    except:
        print("Error connecting to DB in function : 'query_dtts_list' ")
    try:
        data1 = []
        with conn:
            cursor = conn.cursor()
            table_frame = pd.read_sql_query(query,conn)
            values_to_list = table_frame.values.tolist()
            for d in values_to_list:
                data1.append(d[0])
            return data1
    except:
        print("Unexpected error en func 'query_dtts_list': ", sys.exc_info())
        return 'Error en query_dtts_list'

print(query_dtts_list("PROTISA", "exec sp_listar_dtts_control_masivos"))



