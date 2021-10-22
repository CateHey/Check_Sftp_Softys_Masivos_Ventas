import glob
import os,time
from sys import displayhook, path_importer_cache
import zipfile
from py7zr import py7zr
from credentials import *
import pysftp 
import pandas as pd
import numpy as np
import subprocess
from datetime import datetime
from datetime import date
import dateutil
from weekday_validator import diaSemana
from sftp_files import *

def SftpGrupo_Diaz():
    Corporativo = "GRUPO_DIAZ" 
    dia=diaSemana()
    log = ''
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys= None
    myHostname,myUsername,myPassword= getCred(Corporativo)
    info = []

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:
            #print ("Connection succesfully stablished ... ")
            sftp.cwd('/home/cdneg_protisa/Data/')        
            directory_structure = sftp.listdir_attr()
            remoteFile1 = '/home/cdneg_protisa/Data/output_CD.zip'
            remoteFile2 = '/home/cdneg_protisa/Data/output_VYM.zip'
            localfile1 = 'output/output_CD.zip'
            localfile2 = 'output/output_VYM.zip'
            extract ='extrac/'
            password = None
            for attr in directory_structure:
                #print(attr.filename)  
                fecstr = time.strftime("%Y-%m-%d" ,time.localtime(attr.st_mtime))
                fecha = datetime.strptime(fecstr, '%Y-%m-%d').date()
                try:
                    if attr.filename == 'output_CD.zip' and (date.today() - dateutil.relativedelta.relativedelta(months=2)<fecha) and (fecha<=date.today()):
                        sftp.get(remoteFile1,localfile1) 
                        try:                      
                            archivo_zip = zipfile.ZipFile(localfile1,"r")
                            try:
                                print(archivo_zip.namelist())
                                archivo_zip.extractall(path=extract,pwd=password)
                            except:                                    
                                pass
                            archivo_zip.close()   
                        except:
                            try:
                                with py7zr.SevenZipFile(localfile1, mode='r') as archivo_zip:
                                    archivo_zip.extract(targets=[extract])                                   
                            except:
                                try:
                                    ziploc = "C:/Program Files/7-Zip/7z.exe" #location where 7zip is installed
                                    cmd = [ziploc, 'e',localfile1 ,'-o'+ extract ,'-r' ] 
                                    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                                except:
                                    print("error de zipfile")            
                        
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
                                        a = "SOFTYS","GRUPO_DIAZ_CD",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                            else:
                                try:                                         
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):
                                        a = "SOFTYS","GRUPO_DIAZ_CD",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                        except:                     
                            k="Sin Ventas"
                            a = "SOFTYS","GRUPO_DIAZ_CD",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                            info.append(a)

                        ex = 'extrac/*'
                        files = glob.glob(ex)
                        for f in files:
                            os.remove(f)    
                    
    #--------------------------------------------------para vym---------------------------------------------------------------------

                    elif attr.filename == 'output_VYM.zip' and (date.today() - dateutil.relativedelta.relativedelta(months=2)<fecha) and (fecha<=date.today()):
                        sftp.get(remoteFile2,localfile2) 
                        try:                      
                            archivo_zip = zipfile.ZipFile(localfile2,"r")
                            try:
                                print(archivo_zip.namelist())
                                archivo_zip.extractall(path=extract,pwd=password)
                            except:                                
                                pass
                            archivo_zip.close()   
                        except:
                            try:
                                with py7zr.SevenZipFile(localfile2, mode='r') as archivo_zip:
                                    archivo_zip.extract(targets=[extract])                                   
                            except:
                                try:
                                    ziploc = "C:/Program Files/7-Zip/7z.exe" #location where 7zip is installed
                                    cmd = [ziploc, 'e',localfile2 ,'-o'+ extract ,'-r' ] 
                                    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                                except:
                                    print("error de zipfile")            
                        
                        try:
                            rutadf = 'extrac/Ventas.csv'
                            try:
                                df = pd.read_csv(rutadf , header=None ,sep ='|',dtype=np.object0,error_bad_lines=False,encoding_errors='ignore')
                                print(df)
                            except:
                                df=pd.read_csv(rutadf,sep ='|',dtype=np.object0, skiprows=1, header=None,error_bad_lines=False,encoding_errors='ignore')                                                  
                            
                            k=max(df[int("3")])
                            print(k)
                            if dia==0:
                                try:
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=2))):                                                
                                        a = "SOFTYS","GRUPO_DIAZ_VYM",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                            else:
                                try:                                         
                                    fechak = datetime.strptime(k, '%Y-%m-%d').date()
                                    if ((date.today() - dateutil.relativedelta.relativedelta(months=2)) < fechak ) and (fechak < (date.today() -  dateutil.relativedelta.relativedelta(days=1))):
                                        a = "SOFTYS","GRUPO_DIAZ_VYM",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k                                                
                                        info.append(a)
                                except:
                                    print(k,"fecha con error")
                                    pass
                        except:                     
                            k="Sin Ventas"
                            a = "SOFTYS","GRUPO_DIAZ_VYM",attr.filename,attr.st_size, time.strftime("%d-%m-%Y" ,time.localtime(attr.st_mtime)),time.strftime("%H:%M" ,time.localtime(attr.st_mtime)),k
                            info.append(a)

                        ex = 'extrac/*'
                        files = glob.glob(ex)
                        for f in files:
                            os.remove(f)                
                                
                    else:
                        print("========ARCHIVOS APARTE========")
                        print(attr.filename)
                        print("==============================")

                except OSError as err:
                        print("OS error: {0}".format(err))
    return info
            
#columnas =['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','PESOARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA']
#df = pd.DataFrame(info ,columns=columnas) 
#print(df)
#tabla =df.pivot_table(index=['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA'])
#print(tabla)
