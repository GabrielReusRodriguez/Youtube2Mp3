#!/usr/bin/python3

#importing packages
from pytube import YouTube
import os
import sys
import array as arr
import getopt
import time

#Clases
#**************************
class URL():
    def __init__(self, _Url, _Destination, _FileName = None):
        self.url = _Url
        self.destination = _Destination
        self.status = 'Fail'
        if _FileName is not None:
            self.fileName = _FileName
        else:
            self.fileName = None

    def extraeMp3(self):
        startTime = int(round(time.time() * 1000))
        print("\tExtrae Mp3: " + self.url + " \n")
        yt =  YouTube( self.url )
        video = yt.streams.filter(only_audio = True ).first()
        #Download the file
        out_file  = video.download(output_path = self.destination )
        #Renombramos el fichero a .mp3
        if self.fileName is None:
            base, ext = os.path.splitext( out_file )
            new_file= self.destination+"/"+base + '.mp3'
        else:
            new_file = self.destination+"/"+self.fileName +  '.mp3'

        os.rename( out_file, new_file )
        self.status = 'OK'
        endTime = int(round(time.time() * 1000))
        execTime =  endTime - startTime
        print("\t"+yt.title + " se ha descargado correctamente  en formato mp3  en "+ str(execTime)+" ms\n")        


#Funciones
#***************************

def extraeMp3(url , destination, fileName = None ):
    
    print("\tExtrae Mp3: " + url + " \n")
    yt = YouTube( url )
    video = yt.streams.filter(only_audio = True ).first()
    #Download the file
    out_file  = video.download(output_path = destination )
    #Renombramos el fichero a .mp3
    if fileName is None:
        base, ext = os.path.splitext( out_file )
        new_file= self.destination+"/"+base + '.mp3'
    else:
        new_file = fileName +  '.mp3'

    os.rename( out_file, new_file )
    print("\t"+yt.title + " se ha descargado correctamente  en formato mp3")

def printHelp():

    print("Uso de la aplicación: \n ")
    print("\tyoutube2mp3 ")
    print("\tyoutube2mp3 <url> \n")
    print("\tyoutube2mp3 [OPCIONES] <url>\n")
    print("Listado de opciones:\n")
    print("\t\t -f, --fileInput\t: Fichero csv con las urls\n")
    print("\t\t -d, --destinationFolder\t: carpeta donde dejar los mp3\n")
 
    print("\t\t -h, --help\t: muestra esta ayuda\n")

def procesaInputFile(_inputFileName, _destination, _urls,):
    #El fichero sigue el siguiente formato: url,filename
    if os.path.exists(_inputFileName):
        headerLine  = True
        f = open(_inputFileName,"r")
        for line in f:
            if headerLine == False:
                fileName = None
                partes= line.split(",")
                url = partes[0]
                if  len(partes)== 2:
                    fileName = partes[1]
                url = URL(_Url = url, _Destination = _destination, _FileName = fileName )
                urls.append(url)
            else:
                headerLine = False
        f.close()

    else:
        print("Error: el fichero "+_inputFileName+ " NO existe\n")
        return

#Programa principal
#***************************

urls = []
fileInput = None
destination = '.'

if len(sys.argv) == 1:
    #url input del usuario
    myUrl =  input("Introduce la URL del video que quieres descargar: \n >> ")
    #Check for destination to save file
    print("Introduce la carpeta destino ( Deja en blanco para usar el directorio actual )")
    destination = str(input(">> ")) or "."
    url = URL( _Url = myUrl, _Destination = destination )
    urls.append( url )

elif len(sys.argv) == 2:
    myUrl = sys.argv[1]
    url = URL( _Url = myUrl, _Destination = destination )
    urls.append( url )

#elif len(sys.argv ) == 2:
#    myUrl = sys.argv[1]
#    myDestination = sys.argv[2]
#    url = URL( _Url = myUrl, _Destination = myDestination )
#    urls.append( url )

else:
    try:
        options, args  = getopt.getopt(sys.argv[1:], "f:d:h",
                               ["fileInput=",
                                "destinationFolder=",
                                "help"])
        for name, value in options:
            if name  in ['-h', '--help']:
                printHelp()
                exit(1)
            elif name in ['-f', '--fileInput']:
                fileInput = value
            elif name in ['-d', '--destinationFolder']:
                destination = value
        if fileInput is None:
            #No ha venido fichero de input por lo que consideramos que el ultimo parámetro es la url
            myUrl = sys.argv[len(sys.argv)-1]
            url = URL(_Url = myUrl, _Destination = destination)
            urls.append(url)
        else:
            #Procesamos el fichero de input ( fichero separado por comas )
            procesaInputFile( _inputFileName = fileInput, _destination = destination, _urls = urls )
    except getopt.GetoptError as err:
        print("Error al procesar los parámetros "+err+"\n")
        exit (1)

#bucle...
print("Inicio...\n")
print("******************\n")
for nextUrl in urls:
    nextUrl.extraeMp3()
    #extraeMp3( url = nextUrl, destination = myDestination )
print("Proceso finalizado\n")
print("******************\n")