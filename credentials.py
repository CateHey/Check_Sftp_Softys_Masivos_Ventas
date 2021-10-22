
def read_Cred():
    objeto = {
        "PROTISA":{
        "myHostname" : "inteliventas.com",
        "myUsername": "validata4144",
        "myPassword": "foodforthought10",
        "columnafecha": "3",
        "ruta": "/home/validata4144/PROTISA",
        "db_name" : "STRATEGIO_BRUTO_PROTISA",
        "db_password" : "a,udh-ys(DP.ad87912e1w",
        "db_sql_server" : "51.222.82.146",
        "db_username" : "sa"
        },"ARCANGEL":{
        "myHostname" : "inteliventas.com",
        "myUsername": "arcangel_protisa",
        "myPassword": "0x5sWdj.js#-!93MsC-21",
        },
        "CORP_VEGA":{
        "myHostname" : "inteliventas.com",
        "myUsername": "corpvega_protisa",
        "myPassword": "#%ghdy-65d5GBYsd7ybnd-.hx25&/",
        },
        "DIGOSAC":{
        "myHostname" : "inteliventas.com",
        "myUsername": "digosac_vs",
        "myPassword": "4zZkdK44f30U",
        },
        "MARRACHE":{
        "myHostname" : "inteliventas.com",
        "myUsername": "marrache_protisa",
        "myPassword": "#%ghdy-65d5GBYsd7ybnd-.hx25&/",
        },
        "LAGUI":{
        "myHostname" : "inteliventas.com",
        "myUsername": "lagui_protisa",
        "myPassword": ')u0N!"n.sd_,lk?HGHS',
        },
        "GRUPO_DIAZ":{
        "myHostname" : "inteliventas.com",
        "myUsername": "cdneg_protisa",
        "myPassword": "K#d_m!8--O'"+'2&7"2'
        }
    
    }
    return objeto

def getConn(client_name):
    json_object = read_Cred()
    server = json_object[client_name]["db_sql_server"]
    user = json_object[client_name]["db_username"]
    pwd = json_object[client_name]["db_password"]
    db_name = json_object[client_name]["db_name"]
    return server, user, pwd, db_name

def getCred(SFTP):
    objeto  = read_Cred()
    myHostname  = objeto[SFTP]["myHostname"]
    myUsername  = objeto[SFTP]["myUsername"]
    myPassword  = objeto[SFTP]["myPassword"]

    return myHostname,myUsername,myPassword

def getColumn(SFTP):
    objeto  = read_Cred()
    columnafecha  = objeto[SFTP]["columnafecha"]

    return columnafecha
    
def getRuta(SFTP):
    objeto  = read_Cred()
    ruta  = objeto[SFTP]["ruta"]

    return ruta
