from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api, abort
from flask_cors import CORS

# creamos la instancia de flask
app = Flask(__name__)

# creamos la insyancia de mysql
mysql = MySQL()

# creamos la instancia de api de restful
api = Api(app)

CORS(app)


def readcredentials(texto):
    f = open(texto, "r")
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


user_name, password, database_name, server_name = readcredentials("secrets.txt")
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


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# api.add_resource(DetectionList, '/detections', endpoint='detections')
if __name__ == '__main__':
    app.run()
