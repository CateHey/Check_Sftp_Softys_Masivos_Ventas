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

def SftpProtisa():
    Corporativo = "PROTISA" 
    ruta = str(getRuta(Corporativo))
    dia=diaSemana()
    data = query_dtts_list(Corporativo, "exec sp_listar_dtts_control_masivos")
    lend = len(data)
    log = ''
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys= None
    myHostname,myUsername,myPassword= getCred(Corporativo)
    info = []
    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:
        print ("Connection succesfully stablished ... ")            
        for i in range(0,lend):
        # Cambiar a directorio remoto
            print(data[i]) 
            sftp.cwd(ruta+'/'+data[i]+'/')
            # Obtener estructura del directorio
            directory_structure = sftp.listdir_attr()
            remoteFile = ruta+'/'+data[i]+'/output.zip'
            localfile = 'output/output.zip'
            extract ='extrac/'
            password = None
            # Imprimir información
            #print(data[i])
            for attr in directory_structure:
                print(attr.filename)  
                fecstr = time.strftime("%Y-%m-%d" ,time.localtime(attr.st_mtime))
                fecha = datetime.strptime(fecstr, '%Y-%m-%d').date()
                try:
                    if attr.filename == 'output.zip' and (date.today() - dateutil.relativedelta.relativedelta(months=2)<fecha) and (fecha<=date.today()):                       
                                    
                        sftp.get(remoteFile,localfile) 
                        try:                      
                            archivo_zip = zipfile.ZipFile(localfile,"r")
                            try:
                                print(data[i])
                                print(archivo_zip.namelist())
                                archivo_zip.extractall(path=extract,pwd=password)
                            except:                                    
                                pass
                            archivo_zip.close()   
                        except:
                            try:
                                with py7zr.SevenZipFile(localfile, mode='r') as archivo_zip:
                                    archivo_zip.extract(targets=[extract])                                   
                            except:
                                try:
                                    ziploc = "C:/Program Files/7-Zip/7z.exe" #location where 7zip is installed
                                    cmd = [ziploc, 'e',localfile ,'-o'+ extract ,'-r' ] 
                                    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                                except:
                                    print("error de zipfile")            

                        #se lee el Csv de Ventas/ventas                                
                        columnafecha = getColumn(Corporativo)
                        try:                                
                            rutadf = 'extrac/Ventas.csv'  
                            try:
                                df = pd.read_csv(rutadf , header=None ,sep ='|',dtype=np.object0,error_bad_lines=False,encoding_errors='ignore')
                            except:
                                df=pd.read_csv(rutadf,sep ='|',dtype=np.object0, skiprows=1, header=None,error_bad_lines=False,encoding_errors='ignore')

                            k=max(df[int(columnafecha)])
                            if dia==0:
                                try:
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                            
                                        a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                        info.append(a)
                                except:
                                    try:
                                        fechak = datetime.strptime(k, '%Y/%m/%d').date()                                                                       
                                        if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                                
                                            a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                            print(a)
                                            info.append(a)
                                    except:
                                        print(k,"fecha con error")
                                        pass
                            else:
                                try:                                         
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):                                            
                                        a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                        info.append(a)
                                except:
                                    try:
                                        fechak = datetime.strptime(k, '%Y/%m/%d').date()                                                                 
                                        if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):                                                
                                            a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                            info.append(a)
                                    except:
                                        pass
                        except:
                            try:
                                rutadf = 'extrac/ventas.csv'
                                try:
                                    df = pd.read_csv(rutadf , header=None ,sep ='|',dtype=np.object0,error_bad_lines=False,encoding_errors='ignore')
                                    print(df)
                                except:
                                    df=pd.read_csv(rutadf,sep ='|',dtype=np.object0, skiprows=1, header=None,error_bad_lines=False,encoding_errors='ignore')                                                  

                                k=max(df[int(columnafecha)])
                                if dia==0:
                                    try:
                                        fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                        if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                                
                                            a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                            info.append(a)
                                    except:
                                        try:
                                            fechak = datetime.strptime(k, '%Y/%m/%d').date()                                                                       
                                            if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                                    
                                                a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                    
                                                info.append(a)
                                        except:
                                            print(k,"fecha con error")
                                            pass
                                else:
                                    try:                                         
                                        fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                        if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):
                                            a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                            info.append(a)
                                    except:
                                        try:
                                            fechak = datetime.strptime(k, '%Y/%m/%d').date()                                                            
                                            if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):
                                                a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                    
                                                info.append(a)
                                        except:
                                            print(k,"fecha con error")
                                            pass

                            #en caso no se encuentre el csv de ventas por error en el csv o por zip vacío            
                            except:
                                #validacion especial para formato de csv de Estilos
                                if data[i]=="ESTILOS":
                                    if dia==0:
                                        fec= str(date.today() -  dateutil.relativedelta.relativedelta(days=2))
                                    else:
                                        fec= str(date.today() -  dateutil.relativedelta.relativedelta(days=1))
                                    año=fec[0:4]
                                    mes= fec[5:7]
                                    dia= fec[8:10]
                                    fec2="Ventas"+ año+mes+dia
                                    rutadf = 'extrac/{0}.csv'.format(fec2) 
                                    try:
                                        df = pd.read_csv(rutadf , header=None ,sep ='|',dtype=np.object0,error_bad_lines=False,encoding_errors='ignore')
                                        pass
                                    except:
                                        k="Revisar Sftp"
                                        a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                        info.append(a)
                                else:
                                    k="Sin Ventas"
                                    a = Corporativo,data[i],attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                                    info.append(a)

                        #limpiamos carpeta extrac
                        ex = 'extrac/*'
                        files = glob.glob(ex)
                        for f in files:
                            os.remove(f)

                    #imprime archivos aparte                                    
                    else:
                        print("========ARCHIVOS APARTE========")
                        print(attr.filename)
                        print("==============================")

                    #excepción de attr        
                except OSError as err:
                    print("OS error: {0}".format(err))
    return info

#info = SftpProtisa()
#print(info)


