from arcangel import *
from protisa import *
from digosac import *
from corp_vega import *
from lagui import *
from marrache import *
from grupo_diaz import *
info =[]
protisa = SftpProtisa()
arcangel = SftpArcangel()
digosac = SftpDigosac()
corp_vega= SFTPCorp_Vega()
lagui=SFTPLagui()
marrache = SFTPMarrache()
grupo_diaz= SftpGrupo_Diaz()
for attr in protisa:
    info.append(attr)
for attr in arcangel:
    info.append(attr)
for attr in digosac:
    info.append(attr)
""" for attr in corp_vega:
    info.append(attr) """
for attr in lagui:
    info.append(attr)
for attr in marrache:
    info.append(attr)
for attr in grupo_diaz:
    info.append(attr)

columnas =['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','PESOARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA']
df = pd.DataFrame(info ,columns=columnas) 
#print(df)
tabla =df.pivot_table(index=['CORPORATIVO','DISTRIBUIDOR','ARCHIVO','FECHA','HORA','ULTIMAFECHAVENTA'])
print(tabla)
tabla.to_excel('excel/Controlenvio_'+'SOFTYS'+'_SFTP'+'.xlsx',sheet_name='data',startrow=1)