import telepot

def readtoke(texto):
    f = open(texto, "r")
    texto = f.readline()
    print(texto)
    tokenizetext = texto.split()
    return tokenizetext[1]


def sendtxt(token, id, texto):
    bot = telepot.Bot(token)
    bot.sendMessage(id, texto)

def send_messaje(id):
    urlToken = "E:\\resposGit\\FlaskAPIRaptor\\RaptorAlertBot\\teletoken.txt"
    mensaje = "rapaz detectada url: http://localhost:8080/#/"+str(id)
    token = readtoke(urlToken)
    miId = 6382769746
    sendtxt(token, miId, mensaje)
