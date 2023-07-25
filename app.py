from flask import Flask, jsonify, request, Response
from flaskext.mysql import MySQL
from flask_restful import Resource, Api, abort
from flask_cors import CORS
import datetime
import raptorAlerterBot
import os

# creamos la instancia de flask
app = Flask(__name__)

# creamos la insyancia de mysql
mysql = MySQL()

# creamos la instancia de api de restful
api = Api(app)

CORS(app)


def readcredentials(texto):
    directorio_actual = os.path.dirname(__file__)
    print(directorio_actual)
    # Combinar la ruta del directorio actual con la ruta relativa del archivo
    ruta_archivo = os.path.join(directorio_actual, texto)
    print(ruta_archivo)
    f = open(ruta_archivo, "r")
    texto = f.readline()
    tokenizetext = texto.split()
    user_name = tokenizetext[1]
    texto = f.readline()
    tokenizetext = texto.split()
    password = tokenizetext[1]
    texto = f.readline()
    tokenizetext = texto.split()
    database_name = tokenizetext[1]
    texto = f.readline()
    tokenizetext = texto.split()
    server_name = tokenizetext[1]
    f.close()
    return user_name, password, database_name, server_name


user_name, password, database_name, server_name = readcredentials('secrets.txt')
app.config['MYSQL_DATABASE_USER'] = user_name
app.config['MYSQL_DATABASE_PASSWORD'] = password
app.config['MYSQL_DATABASE_DB'] = database_name
app.config['MYSQL_DATABASE_HOST'] = server_name

# inicializamos la extension de MySQL
mysql.init_app(app)

'''
class DetectionList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from detections""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
'''


@app.route('/gets')
def get():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""select * from detections""")
        rows = cursor.fetchall()
        if rows:
            print(rows)
            diccionario = {"id": rows[0][0], "fecha": rows[0][1], "userIdT": rows[0][2], "url": rows[0][3]}
            return jsonify(diccionario)
        else:
            abort(404, message="Todo {} doesn't exist")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/imagen', methods=['POST'])
def get_image():
    if request.method == 'POST':
        if 'id' in request.headers:
            id = request.headers['id']
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("""select * from detections WHERE idDetection=%s""", id)
                rows = cursor.fetchall()
                if len(rows) > 0:
                    diccionario = {"id": rows[0][0], "fecha": rows[0][1], "userIdT": rows[0][2], "url": rows[0][3]}
                    return jsonify(diccionario)
                else:
                    abort(404, message="error id miss")
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
        else:
            abort(404, message="id error")
    else:
        abort(404, message="method error")


def get_max_id_detections():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT idDetection FROM detections ORDER BY idDetection DESC LIMIT 1""")
    row = cursor.fetchall()
    if (len(row) > 0):
        return row[0][0]
    else:
        return -1


@app.route('/addimagen', methods=['POST'])
def add_imagen():
    if request.method == 'POST':
        if 'dateDetection' in request.headers:
            if 'IdTelegramUser' in request.headers:
                if 'urlImagen' in request.headers:
                    dateImagen = datetime.datetime.strptime(request.headers['dateDetection'], '%Y-%m-%d %H:%M:%S.%f')
                    id = int(request.headers['IdTelegramUser'])
                    url = request.headers['urlImagen']
                    preid = get_max_id_detections()
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO detections (dateDetection, IdTelegramUser, urlImagen)
VALUES(%s ,%s,%s)""", (dateImagen, id, url))
                    conn.commit()
                    postid = get_max_id_detections()
                    if preid < postid:
                        print(str(dateImagen) + "- -" + str(id) + "- -" + "- -" + url + "- id:" + str(postid))
                        raptorAlerterBot.send_messaje(postid)
                        return Response("{'a':'b'}", status=201, mimetype='application/json')
                    else:
                        abort(500, message="error data base")
                else:
                    abort(404, message="url error")
            else:
                abort(404, message="id error")
        else:
            abort(404, message="date error")
    else:
        abort(404, message="method error")


@app.route('/save_validation', methods=['POST'])
def save_validation():
    if request.method == 'POST':
        if not ('idDetection' in request.headers):
            abort(404, message="id error")
        if not ('selectedOption' in request.headers):
            abort(404, message="option error")
        if not ('comments' in request.headers):
            abort(404, message="comments error")
        id = int(request.headers['idDetection'])
        option = int(request.headers['selectedOption'])
        comment = request.headers['comments']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO validations (idDetection, selectedOption, comments)
        VALUES(%s ,%s,%s)""", (id, option, comment))
        conn.commit()
        return Response("{'a':'b'}", status=201, mimetype='application/json')
    else:
        abort(404, message="method error")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# api.add_resource(DetectionList, '/detections', endpoint='detections')
if __name__ == '__main__':
    app.run()
