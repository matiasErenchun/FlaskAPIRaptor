from Interfaces.DetectionsInterfaceFile import DetectionsInterface


class DetectionsRepository(DetectionsInterface):
    def __init__(self, conexion):
        self.conn = conexion
        self.types = ['ave_volando', 'ave_posada', 'ave_tierra', 'ave_rapaz_volando', 'ave_rapaz_posada',
                      'ave_rapaz_tierra']

    def save_detection(self, id_telegram, date, url_image, source, detection_class):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO detections (dateDetection, IdTelegramUser, urlImagen, source, class)
            VALUES(%s ,%s,%s,%s,%s)""", (date, id_telegram, url_image, source, detection_class))
            self.conn.commit()
        except Exception as e:
            print(e)
            raise Exception()

    def get_detection(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""select * from detections WHERE id=%s""", id)
        rows = cursor.fetchall()
        return rows

    def get_all_detections(self, source, filter_class):
        cursor = self.conn.cursor()
        if source == 'RaptorDetector' or source == 'BirdDetector':
            if filter_class in self.types:
                cursor.execute("""select * from detections where source=%s and class=%s """, (source, filter_class))
            elif filter_class == "All":
                cursor.execute("""select * from detections where source=%s """, source)
        elif filter_class in self.types:
            cursor.execute("""select * from detections where class=%s """,  filter_class)
        else:
            cursor.execute("""select * from detections""")
        rows = cursor.fetchall()
        return rows

    def get_max_id_detections(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id FROM detections ORDER BY id DESC LIMIT 1""")
        row = cursor.fetchall()
        if len(row) > 0:
            return row[0][0]
        else:
            return -1
