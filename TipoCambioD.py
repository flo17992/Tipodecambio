import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import plotly.express as px
import os
from os.path import exists
import time
import kaleido


#borra los archivos anterioes csv en la carpeta de descargas o downloads
if os.path.exists('C:/Users/61055/Downloads/histórico_rango.csv'):

    os.remove('C:/Users/61055/Downloads/histórico_rango.csv')


#Abre el webdriver de chrome en el desktop
driver = webdriver.Chrome("C:/Users/61055/Desktop/chromedriver.exe")


#Se va a la pagina del Banguat para ver el tipo de cambio
driver.get("https://www.banguat.gob.gt/tipo_cambio/")


#Encuentra la caja de tasa de cambio y la vacia
item = driver.find_element(By.ID, "fecha_apartir").clear()
item = driver.find_element(By.ID, "fecha_apartir")


#Calcula la fecha de hoy le quita un mes y la cambia a formato dia/mes/año
today = date.today()
today = today - relativedelta(months=1)
d1 = today.strftime("%d/%m/%Y")


#Inserta la fecha ya cambiada en la caja de texto de la fecha inicial del rango de tipo de cambio
item.send_keys(d1)


#hace enter dentro de la caja de tipo de cambia
item.send_keys(Keys.ENTER)


#busca la dirección del boton de descarga y descarga el archivo
content = driver.find_element(By.XPATH, "/html/body/div/div/div/button")
driver.execute_script("arguments[0].click();", content)


#Pausa 1 segundo para esperar que descargue el archivo
time.sleep(1)


#Lee el archivo csv descargado
df = pd.read_csv('C:/Users/61055/Downloads/histórico_rango.csv')


#Limpia el archivo csv 
df = df.iloc[3:len(df.iloc[:,1])-5,0:2]
df = df.rename(columns={'Tipo de Cambio: Dólares de EE.UU.':'Fecha','Unnamed: 1':'Tipo_cambio'})
df = df.reset_index()


#Genera la grafica con sus caracteristicas
fig = px.line(df, x='Fecha', y="Tipo_cambio", markers=True,color_discrete_sequence=['#003964'])
fig.update_traces(line=dict( width= 5),marker=dict(size=12))
fig.update_yaxes(title_text='Tipo de Cambio', ticklabelstep = 2)

fig.write_image("//10.2.200.212/0003 informacion temporal/Tipo_de_Cambio.svg")

#fin


