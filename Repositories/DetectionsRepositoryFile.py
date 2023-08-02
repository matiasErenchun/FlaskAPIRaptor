from Interfaces.DetectionsInterfaceFile import DetectionsInterface


class DetectionsRepository(DetectionsInterface):
    def __init__(self, conexion):
        self.conn = conexion

    def save_detection(self, id_telegram, date, url_image):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO detections (dateDetection, IdTelegramUser, urlImagen)
            VALUES(%s ,%s,%s)""", (date, id_telegram, url_image))
            self.conn.commit()
        except Exception as e:
            print(e)
            raise Exception()

    def get_detection(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""select * from detections WHERE id=%s""", id)
        rows = cursor.fetchall()
        return rows

    def get_all_detections(self):
        pass

    def get_max_id_detections(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id FROM detections ORDER BY id DESC LIMIT 1""")
        row = cursor.fetchall()
        if len(row) > 0:
            return row[0][0]
        else:
            return -1
