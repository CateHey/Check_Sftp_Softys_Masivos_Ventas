import glob
import os,time
from sys import displayhook, path_importer_cache
import zipfile
from py7zr import py7zr
from credentials import getRuta
from credentials import getColumn
import pysftp 
import pandas as pd
import numpy as np
import subprocess
from datetime import datetime
from datetime import date
import dateutil
from weekday_validator import diaSemana
from sftp_files import *

def SFTPCorp_Vega():
    Corporativo = "CORP_VEGA" 
    dia=diaSemana()
    log = ''
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys= None
    myHostname,myUsername,myPassword= getCred(Corporativo)
    info = []

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:
            #print ("Connection succesfully stablished ... ")
            sftp.cwd('/home/corpvega_protisa/DATA/')        
            directory_structure = sftp.listdir_attr()
            remoteFile = '/home/corpvega_protisa/DATA/Ventas.csv'
            localfile = 'extrac/Ventas.csv'
            password = None
            for attr in directory_structure:
                #print(attr.filename)  
                fecstr = time.strftime("%Y-%m-%d" ,time.localtime(attr.st_mtime))
                fecha = datetime.strptime(fecstr, '%Y-%m-%d').date()
                try:
                    if attr.filename == 'Ventas.csv' and (date.today() - dateutil.relativedelta.relativedelta(months=2)<fecha) and (fecha<=date.today()):                       
                                        
                        sftp.get(remoteFile,localfile)        
                        try:
                            rutadf = 'extrac/Ventas.csv'
                            try:
                                df = pd.read_csv(rutadf , header=None ,sep ='|',dtype=np.object0,error_bad_lines=False,encoding_errors='ignore')
                                #print(df)
                            except:
                                df=pd.read_csv(rutadf,sep ='|',dtype=np.object0, skiprows=1, header=None,error_bad_lines=False,encoding_errors='ignore')                                                  

                            k=max(df[int("3")])
                            #print(k)
                            if dia==0:
                                try:
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                                
                                        a = "SOFTYS","CORP_VEGA",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                            else:
                                try:                                         
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):
                                        a = "SOFTYS","CORP_VEGA",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                        except:                     
                            k="Sin Ventas"
                            a = "SOFTYS","CORP_VEGA",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                            info.append(a)

                        ex = 'extrac/*'
                        files = glob.glob(ex)
                        for f in files:
                            os.remove(f)
                                
                    else:
                        pass

                except OSError as err:
                        print("OS error: {0}".format(err))
    return info

#columnas =['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','PESOARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA']
#df = pd.DataFrame(info ,columns=columnas) 
#print(df)
#tabla =df.pivot_table(index=['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA'])
#print(tabla)