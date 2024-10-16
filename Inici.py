import os
import streamlit as st
from openai import OpenAI
import app_component as au
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sys
import speech_recognition as sr
import random
import mysql.connector
import requests
import ftplib
import time




db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name =  st.secrets["DB_NAME"]
db_user =  st.secrets["DB_USER"]
db_password =  st.secrets["DB_PASSWORD"]

client = OpenAI(api_key=st.secrets["auto_pau"])


parlantTema = ''
parlantCrea = ''
parlantID = 0
parlantTemaID = 0
parlantPregunta = ''
pregunta = 0

st.image("curiosaipromptformula.png", caption="La fórmula del prompt para Dalle-3")
with st.form("images_form"):
  text = st.text_area("Escribe un prompt con la estructura adecuada para CuriosAI..." )
  submit_button = st.form_submit_button(label="Generar Imagen")

if submit_button:
  st.write("Generando Imagen...")

  response = client.images.generate(
      model="dall-e-3",
      prompt="Haz una imagen" + " a partir de esta descripción:" + text + ".",
      size="1024x1024",
      quality="standard",
      n=1
  )
  for i in range(1):
    url = response.data[i].url
    st.image(url, caption=f"Prompt CuriosAI: {text}", use_column_width=True)
    res = requests.get(response.data[0].url)
    missatge ="Descriu una imatge..."
    if parlantTemaID <= 0:
        parlantTemaID = 3880329

    if parlantID <= 0:
        parlantID = 3861769

    creaName = str(parlantID) + "_" + str(time.time()) + "_" + str(parlantTemaID) + ".jpg"
    with open(creaName, 'wb') as f:
        f.write(res.content)

    # Crea una conexión con la base de datos
    conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user,
                                       password=db_password)

    # Crea un cursor para ejecutar comandos SQL
    cur = conn.cursor()

     # Ejecuta una consulta SQL
    sql = "INSERT INTO teclaCOMIC (id,autora,url,final,escena,descripcio,tema) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    valores = (parlantID, 'curiosai prompt',creaName, 0, missatge, text, parlantTemaID)
    cur.execute(sql, valores)

    # Obtiene los resultados de la consulta
    results_database = cur.fetchall()
    conn.commit()

    # Cierra la conexión con la base de datos
    cur.close()
    conn.close()
    ftp_server = ftplib.FTP(st.secrets["PA_FTP"], st.secrets["PA_FTPUSER"], st.secrets["PA_COD"])
    file = open(creaName, 'rb')  # file to send
    print('ok2')
    # Read file in binary mode
    ftp_server.storbinary('STOR ' + creaName, file)
    print('ok3')
    ftp_server.quit()
    print('ok4')
    file.close()  # close file and FTP
    pregunta = pregunta + 1
