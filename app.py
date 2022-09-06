##########################################################################
################################# MY API #################################
##########################################################################
##########################  BY: JAIRONEUS@GMAIL>COM ######################
##########################################################################
##########################################################################


### Librerias necesarias para el funcionamiento del API
from ast import Return, Try
from os import abort
from xml.dom.minidom import Identified
from flask import Flask, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import jsonify
from urllib.request import urlopen
### Funciones propias
from funciones import crear_archivo, escribir_archivo, buscar_palabra

# Crea el objeto MYAPY
myapi = Flask(__name__)

###########################################################################################
####################### ENDPOINT BUSCAR PALABRA ###########################################
###########################################################################################
## Mediante este endpoint busca la palabra indicada en un archivo de google con ID indicado
## Para consumir el servicio es necesario realizar una peticion de tipo GET
## Hacia la direccion donde se expone la API, la ruta /search y enviar el parametro palabra
## por ejemplo http://127.0.0.1:5000/wsqhi72827368e236876238?palabra=casa
## http://127.0.0.1:5000/(id del archivo a consultar)?palabra=(palabra a consultar)
###########################################################################################
#         PARAMETROS:
#                      1. Palabra: es la palabra a buscar, se envia en la peticion GET
#                      2. ID: Es el identificador del archivo donde se buscara la palabra
#                        Se envia a traves de la URL.
#         RESPUESTA:
#                   Mensaje 200 OK si la palabra existe en el archivo con ID indicado
#                   Mensaje 500 si la palabra no existe en el archivo con ID indicado
#
###########################################################################################
@myapi.route('/search/<identificador>')
def search(identificador):
    # extrae la palabra del parametro enviado en el request
    palabra = request.args.get('palabra')
    #Llama la funcion BUSCAR PALABRA y almacena el resultado en una variable
    # La funcion BUSCAR palabra recibe la palabra a buscar y el ID del archivo
    # La funcion BUSCAR PALABRA regresa una cadena con texto FALLIDO Si la palabra 
    # NO existe dentro del archivo con ID indicado
    # La funcion BUSCAR PALABRA regresa una cadena con texto EXITOSO Si la palabra 
    # existe dentro del archivo con ID indicado
    existe = buscar_palabra(palabra,identificador)
    #Valida el resultado de la funcion BUSCAR palabra
    if existe == "FALLIDO":
        #Si el resultado es FALLIDO responde con 500
        return 'palabra no encontrada', 500
    elif existe == "EXITOSO": 
        #Si el resultado es PALABRA ENCONTRADA envia respuesta de 200 Ok
        return 'palabra encontrada', 200
###############################################################################################
#Mediante esta ruta se permite la creacion de un nuevo archivo y se escribe el texto ingresado.
# Parametros:
#               1. titulo: Nombre que se le dara al archivo
#               2. descripcion: Texto que se escribira en el archivo
# Respuesta: La respuesta se da en formato JSON
#            1. titulo: Nombre que se le dara al archivo
#            2. descripcion: Texto que se escribira en el archivo  
#            3. ID del archivo creado
###############################################################################################
@myapi.route('/file', methods = ['POST'])
def file():
    if request.method == 'POST':
        #extrae los datos del JSON enviado en la peticion POST
        datos_json = request.get_json()
        ##########################
        #Valida la existencia de el parametro titulo en el JSON  
        if "titulo" in datos_json:
            #Valida la existencia de el parametro descripcion en el JSON
            if "descripcion" in datos_json:
                # extrae el valor del parametro TITULO del JSON
                titulo_archivo = datos_json["titulo"]
                if len(titulo_archivo) != 0:
                    # extrae el valor del parametro DESCRIPCION del JSON
                    descripcion_archivo = datos_json["descripcion"]
                    #llama la funcion crear_archivo para crear un doc en drive 
                    #Recibe como parametro el titulo y devuelve el id del archivo creado
                    id_nuevo_archivo = crear_archivo(titulo_archivo)
                    #valida si el archivo fue creado
                    if id_nuevo_archivo == "No hay ID":
                        return '', 500
                    else:
                        #Se pone el texto ingresado por el usuario en el archivo creado
                        escribir_archivo(id_nuevo_archivo,descripcion_archivo)
                        #Envia el resultado en formato JSON
                        return jsonify(
                            id = id_nuevo_archivo,
                            titulo = titulo_archivo,
                            descripcion = descripcion_archivo)
                else:
                    return '', 500
            else:
                return '', 404
        else:
            return '', 404


        

# Ejecuta la API
if __name__ == '__main__':
    myapi.run()
