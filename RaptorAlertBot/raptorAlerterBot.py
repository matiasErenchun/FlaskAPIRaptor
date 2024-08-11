import telepot
import os

def readtoke(texto):
    directorio_actual = os.path.dirname(__file__)
    # print(directorio_actual)
    # Combinar la ruta del directorio actual con la ruta relativa del archivo
    ruta_archivo = os.path.join(directorio_actual, texto)
    f = open(ruta_archivo, "r")
    texto = f.readline()
    print(texto)
    tokenizetext = texto.split()
    return tokenizetext[1]


def sendtxt(token, id, texto):
    bot = telepot.Bot(token)
    bot.sendMessage(id, texto)

def send_messaje(id):
    urlToken = "teletoken.txt"
    mensaje = "rapaz detectada url: http://localhost:8080/"+str(id)
    token = readtoke(urlToken)
    miId = 6382769746
    sendtxt(token, miId, mensaje)
