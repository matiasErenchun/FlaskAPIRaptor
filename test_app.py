import unittest
from unittest.mock import patch
from app import app
from flask import jsonify
from RaptorAlertBot.raptorAlerterBot import send_message

class TestGetAllImagesEndpoint(unittest.TestCase):

    @patch('app.get_db')
    def test_get_all_images_endpoint(self, mock_get_db):
        # Configurando el mock de la base de datos
        mock_conn = mock_get_db.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Configurando el comportamiento esperado del mock
        mock_cursor.execute.return_value = [("url1", "class1"), ("url2", "class2")]

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/getsAll', headers={
            'page': '1',
            'beginning': '2023-01-01T00:00:00.000Z',
            'end': '2023-01-02T00:00:00.000Z',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud fue exitosa
        self.assertEqual(response.status_code, 200)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_get_all_images_endpoint_DB_error(self, mock_detections_repository, mock_get_db):
        # Configurando el mock de la base de datos para simular un error
        mock_conn = mock_get_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.side_effect = Exception("Simulated database error")

        # Configurando el mock de DetectionsRepository para simular un error
        mock_detections_instance = mock_detections_repository.return_value
        mock_detections_instance.get_all_detections.side_effect = Exception("Simulated DetectionsRepository error")

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/getsAll', headers={
            'page': '1',
            'beginning': '2023-01-01T00:00:00.000Z',
            'end': '2023-01-02T00:00:00.000Z',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud generó un error interno del servidor
        self.assertEqual(response.status_code, 500)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_missing_page_header(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba sin el encabezado 'page'
        response = app.test_client().post('/getsAll', headers={
            'beginning': '2023-01-01T00:00:00.000Z',
            'end': '2023-01-02T00:00:00.000Z',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud genere un error 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        # También puedes verificar el contenido del mensaje de error si tu aplicación devuelve detalles sobre el error.

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_wrong_method(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba con un método incorrecto (GET en lugar de POST)
        response = app.test_client().get('/getsAll', headers={
            'page': '1',
            'beginning': '2023-01-01T00:00:00.000Z',
            'end': '2023-01-02T00:00:00.000Z',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud genere un error 405 (Method Not Allowed)
        self.assertEqual(response.status_code, 405)
        # También puedes verificar el contenido del mensaje de error si tu aplicación devuelve detalles sobre el error.


class TestGetImageEndpoint(unittest.TestCase):

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_get_image_wrong_method(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba con un método incorrecto
        response = app.test_client().get('/imagen', headers={'id': '1'})

        # Asegurándose de que la solicitud devuelva un error 405 (Method Not Allowed)
        self.assertEqual(response.status_code, 405)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_get_image_missing_id(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba sin proporcionar el header 'id'
        response = app.test_client().post('/imagen', headers={})

        # Asegurándose de que la solicitud devuelva un error 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')  # Mock DetectionsRepository
    def test_get_image_internal_server_error(self, mock_detections_repository, mock_get_db):
        # Configurando el mock de la base de datos para simular un error interno
        mock_conn = mock_get_db.return_value
        mock_conn.cursor.side_effect = Exception("Simulated internal server error")

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/imagen', headers={'id': '1'})

        # Asegurándose de que la solicitud devuelva un error 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)


class TestAddDetectionEndpoint(unittest.TestCase):

    @patch('app.get_db')
    @patch('app.DetectionsRepository')
    def test_get_all_images_missing_headers(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba sin incluir los headers requeridos
        response = app.test_client().post('/getsAll', headers={})

        # Asegurándose de que la solicitud devuelve un error 404 (Not Found) porque faltan headers
        self.assertEqual(response.status_code, 404)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')
    def test_get_all_images_internal_server_error(self, mock_detections_repository, mock_get_db):
        # Configurando el mock de la base de datos para lanzar una excepción simulando un error interno del servidor
        mock_detections_repository.return_value.get_all_detections.side_effect = Exception('Simulated internal error')

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/getsAll', headers={
            'page': '1',
            'beginning': '2023-01-01T00:00:00.000Z',
            'end': '2023-01-02T00:00:00.000Z',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud devuelve un error 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')
    def test_add_detection_invalid_method(self, mock_detections_repository, mock_get_db):
        # Realizando la solicitud con un método incorrecto
        response = app.test_client().get('/addDetecction')

        # Asegurándose de que la solicitud fue rechazada por un método no permitido (código de estado 405)
        self.assertEqual(response.status_code, 405)

    @patch('app.get_db')
    @patch('app.DetectionsRepository')
    @patch('app.raptorAlerterBot.send_message')
    def test_add_detection_success(self, mock_send_message, mock_detections_repository, mock_get_db):
        # Configurando el mock de la base de datos
        mock_conn = mock_get_db.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Configurando el comportamiento esperado del mock
        mock_cursor.execute.return_value = None
        mock_detections_repository.return_value.save_detection.return_value = None
        mock_detections_repository.return_value.get_max_id_detections.return_value = 123

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/addDetecction', headers={
            'dateDetection': '2023-01-01 12:00:00',
            'IdTelegramUser': '123',
            'urlImagen': 'url1',
            'source': 'source1',
            'class': 'class1'
        })

        # Asegurándose de que la solicitud fue exitosa (código de estado 201)
        self.assertEqual(response.status_code, 201)
        # También puedes verificar el contenido del cuerpo de la respuesta si tu aplicación devuelve detalles.
        # Por ejemplo, asumiendo que la aplicación devuelve un JSON, puedes hacer algo como:
        expected_response = {'a': 'b'}
        self.assertDictEqual(expected_response, response.get_json())
        # Verifica que la función send_message fue llamada
        mock_send_message.assert_called_with(123)


class TestGetValidationEndpoint(unittest.TestCase):

    @patch('app.get_db')
    @patch('app.ValidationResultRepository')
    def test_get_validation_missing_id_header(self, mock_validation_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba sin incluir el header 'id'
        response = app.test_client().post('/validation', headers={})

        # Asegurándose de que la solicitud devuelve un error 404 (Not Found) porque falta el header 'id'
        self.assertEqual(response.status_code, 404)

    @patch('app.get_db')
    @patch('app.ValidationResultRepository')
    def test_get_validation_method_not_allowed(self, mock_validation_repository, mock_get_db):
        # Realizando la solicitud al endpoint de prueba con un método no permitido
        response = app.test_client().get('/validation', headers={'id': '1'})

        # Asegurándose de que la solicitud devuelve un error 405 (Method Not Allowed)
        self.assertEqual(response.status_code, 405)

    @patch('app.get_db')
    @patch('app.ValidationResultRepository')
    def test_get_validation_internal_server_error(self, mock_validation_repository, mock_get_db):
        # Configurando el mock de la base de datos para lanzar una excepción simulando un error interno del servidor
        mock_validation_repository.return_value.get_validation_result_by_id.side_effect = Exception(
            'Simulated internal error')

        # Realizando la solicitud al endpoint de prueba
        response = app.test_client().post('/validation', headers={'id': '1'})

        # Asegurándose de que la solicitud devuelve un error 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
