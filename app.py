from flask import Flask, jsonify, request, Response, g
from flaskext.mysql import MySQL
from flask_restful import Api, abort
from flask_cors import CORS
import datetime
import os
from RaptorAlertBot import raptorAlerterBot
from Repositories.ValidationResultRepositoryFile import ValidationResultRepository
from Repositories.DetectionsRepositoryFile import DetectionsRepository

# creamos la instancia de flask
app = Flask(__name__)

# creamos la insyancia de mysql
mysql = MySQL()


def get_db():
    if 'db' not in g:
        # Crear una nueva conexión y agregarla al contexto de la aplicación
        g.db = mysql.connect()
    return g.db


@app.teardown_appcontext
def close_db(exception):
    # Cerrar la conexión cuando se termina el contexto de la aplicación
    db = g.pop('db', None)
    if db is not None:
        db.close()


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


# codigos de respuesta https://developer.mozilla.org/es/docs/Web/HTTP/Status agregar a documento.
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
    if request.method != 'POST':
        abort(405, message="method error")
    if not ('id' in request.headers):
        abort(404, message="id error")
    id_detection = request.headers['id']
    try:
        conn = get_db()
        dection_result = DetectionsRepository(conn)
        rows = dection_result.get_detection(id_detection)
        if len(rows) > 0:
            diccionario = {"id": rows[0][0], "fecha": rows[0][1], "userIdT": rows[0][2], "url": rows[0][3]}
            return jsonify(diccionario)
        else:
            abort(404, message="error id miss")
    except Exception as e:
        print(e)


@app.route('/addDetecction', methods=['POST'])
def add_detecction():
    if request.method != 'POST':
        abort(405, message="method error")
    if not ('dateDetection' in request.headers):
        abort(404, message="date error")
    if not ('IdTelegramUser' in request.headers):
        abort(404, message="id error")
    if not ('urlImagen' in request.headers):
        abort(404, message="url error")

    date_imagen = datetime.datetime.strptime(request.headers['dateDetection'], '%Y-%m-%d %H:%M:%S.%f')
    telegram_user_id = int(request.headers['IdTelegramUser'])
    url = request.headers['urlImagen']
    try:
        conn = get_db()
        dection_result = DetectionsRepository(conn)
        dection_result.save_detection(telegram_user_id, date_imagen, url)
        postid = dection_result.get_max_id_detections()
        print(str(telegram_user_id) + "- -" + str(id) + "- -" + "- -" + url + "- id:" + str(postid))
        raptorAlerterBot.send_messaje(postid)
        return Response("{'a':'b'}", status=201, mimetype='application/json')
    except Exception as e:
        abort(500, message="Internal Server Error")


@app.route('/save_validation', methods=['POST'])
def save_validation():
    if request.method != 'POST':
        abort(405, message="Method Not Allowed")
    if not ('idDetection' in request.headers):
        abort(404, message="id error")
    if not ('selectedOption' in request.headers):
        abort(404, message="option error")
    if not ('comments' in request.headers):
        abort(404, message="comments error")
    id_detection = int(request.headers['idDetection'])
    option = int(request.headers['selectedOption'])
    comment = request.headers['comments']
    try:
        conn = get_db()
        validation_result = ValidationResultRepository(conn)
        validation_result.save_validation_result(id_detection, option, comment)
        return Response("{'a':'b'}", status=201, mimetype='application/json')
    except Exception as e:
        abort(500, message="Internal Server Error")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# api.add_resource(DetectionList, '/detections', endpoint='detections')
if __name__ == '__main__':
    app.run()
