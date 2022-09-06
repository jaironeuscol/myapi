##########################################################################
################################# MY API #################################
##########################################################################
##########################  BY: JAIRONEUS@GMAIL>COM ######################
##########################################################################
##########################################################################

### Librerias necesarias para el funcionamiento del los metodos

from __future__ import print_function
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

#Alcance para la autenticacion en DRIVE
SCOPES = ['https://www.googleapis.com/auth/drive']

#Alcance de la aplicacion en DOCS
SCOPESDOCS = ['https://www.googleapis.com/auth/documents']


#######################################################################################
#######################################################################################
#          Funcion para la creacion de un Documento en drive, 
#          PARAMETROS:
#                       1. Nombre del archivo a crear
#          RESULTADO:  
#                       1. ID del archivo creado
#######################################################################################
def crear_archivo(nombre_archivo):
    creds = None
    id_archivo= "No hay ID"
    #valida si existe credenciales
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #valida si las credenciales son validas o expiraron
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        #Si no existen el token crea un flujo para crearlo    
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        #almacena el token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        # create el nombre y tipo de archivo
        file_metadata = {
            'name': nombre_archivo,
            'mimeType': 'application/vnd.google-apps.document' 
        }
    
        #crear el archivo
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(F'\nEl archivo ha sido creado con ID: "{file.get("id")}".')
        id_archivo = file.get('id')

    #manejo de errores
    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
    #Retorna el ID del archivo creado
    return(id_archivo)


#######################################################################################
#######################################################################################
#          Funcion para escribir texto en un documento de drive 
#          PARAMETROS:
#                       1. Identificador del documento
#                       2. Texto a escribir en el documento
#
#######################################################################################
def escribir_archivo(id_archivo, texto):
    creds2 = None
    #valida si existe credenciales
    if os.path.exists('token2.json'):
        creds2 = Credentials.from_authorized_user_file('token2.json', SCOPES)
    #valida si las credenciales son validas o expiraron
    if not creds2 or not creds2.valid:
        if creds2 and creds2.expired and creds2.refresh_token:
            creds2.refresh(Request())
        #Si no existen el token crea un flujo para crearlo    
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds2 = flow.run_local_server(port=0)
        #almacena el token
        with open('token2.json', 'w') as token:
            token.write(creds2.to_json())
    try:
        # create drive api client
        service = build('docs', 'v1', credentials=creds2)
        #texto a insertar
        requests = [
             {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': texto
                }
            }
        ]
        #inserta el texto
        result = service.documents().batchUpdate(documentId=id_archivo, body={'requests': requests}).execute()
        print(F'\nEl archivo con id: '+ id_archivo + 'fue escrito correctamente')
    #manejo de errores
    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

#######################################################################################
#######################################################################################
#          Funcion para buscar palabra en un archivo con identificador dado
#          PARAMETROS:
#                       1. Palabra a buscar
#                       2. identificador del archivo
#          RESULTADO: 
#                       1. Cadena de texto con:
#                           1.1. EXITOSO si la palabra fue encontrada
#                           1.2. FALLIDO si el ID o la palabra no fueron encontrados
#######################################################################################
def buscar_palabra(palabra, real_id):
    creds = None
    c = 0
    # Crea el QUERY para la consulta de la palabra
    cadena = "fullText contains '"+palabra+"'"
    #valida si existe credenciales
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #valida si las credenciales son validas o expiraron
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        #Si no existen el token crea un flujo para crearlo    
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        #almacena el token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Inicia la validacion de la palabra dentro del archivo con ID especificado
    try:
        #crea cliente api drive
        service = build('drive', 'v3', credentials=creds)   
        files = []
        file_id = real_id
        page_token = None
        # Inicia ciclo para ir cargando los documentos y validar el ID y la palabra
        while True:
            #valida si en el archivo existe la palabra buscada
            response = service.files().list(q = cadena ,
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                id = file.get("id")
                # SI el id es igual al indicado marca como exitosa la busqueda
                if id == file_id:
                    #print(F'Found file: {file.get("name")}, {file.get("id")}')
                    resultado_buscar_palabra = "EXITOSO"
                    #se alimenta el contador de resultados exitosos para la existencia del ID
                    c = c+1
            # Valida si el resultado de la busqueda de ID arrojo algun resultado
            if c==0:
                # si la busqueda de ID no arrojo resultados se marca el resultado de la busqueda total como FALLIDO
                resultado_buscar_palabra = "FALLIDO"
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    #MAnejo de errores
    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
    #Retorna el resultado de la busqueda
    return(resultado_buscar_palabra)


