from Interfaces.ValidationResultInterfaceFile import ValidationResultInterface


class ValidationResultRepository(ValidationResultInterface):
    def __init__(self, conexion):
        self.conn = conexion

    def save_validation_result(self, id_detection, option, comment):
        # se peuden agregar mucha mas logica, con respecto a la validacion de los campos para evitar posibles ataques.
        # por otra parte tanbien se puede mejorar el manejo de lso errores
        try:

            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO validations (id_detection, selectedOption, comments)
                    VALUES(%s ,%s,%s)""", (id_detection, option, comment))
            self.conn.commit()
            return id_detection
        except Exception as e:
            print(e)
            raise Exception()

    def get_all_validations_result(self):
        pass

    def get_validation_result_by_id(self, id_validation):
        pass
