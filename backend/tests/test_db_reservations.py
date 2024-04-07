import http
import unittest
import sys
from pathlib import Path
# Add the parent directory to sys.path
current_dir = Path(__file__).resolve()  # Absolute path of the current file
parent_dir = current_dir.parent.parent  # Get the parent directory
sys.path.append(str(parent_dir))

from http.server import HTTPServer
from server import RequestHandler
import json
import threading
from datetime import datetime


import http.client

class TestServerReservations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8010)
        cls.server = HTTPServer(cls.server_address, RequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
    

    def test_get_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('GET', '/reservations')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        # Add your assertions for the specific data you expect to receive

    def test_insert_reservation(self):
        # Connect to the server and send a POST request to insert a reservation record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        serialized_dt = datetime(2024, 12, 21, 20, 30).isoformat()
        reservation_data = {'customer_id': 1, 'table_id': 1,  'date_time': serialized_dt,'guests': 4,}
        connection.request('POST', '/reservations', json.dumps(reservation_data), headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data['message'], 'Reservation inserted successfully')

    def test_get_by_id_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('GET', '/reservations/1')  # Replace '1' with the desired reservation ID
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        # Add your assertions for the specific data you expect to receive

    def test_update_reservation(self):
        # Connect to the server and send a PUT request to update a reservation record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        serialized_dt = datetime(2024, 12, 21, 18, 30).isoformat()
        reservation_data = {'reservation_id': 1, 'date_time': serialized_dt, 'guests': 6}
        connection.request('PUT', '/reservations', json.dumps(reservation_data), headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data['message'], 'Reservation updated successfully')

    def test_update_reservation(self):
        # Connect to the server and send a PUT request to update a reservation record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        reservation_data = {'reservation_id': 1, 'status': 'Completed'}
        connection.request('PUT', '/reservations', json.dumps(reservation_data), headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data['message'], 'Reservation status updated successfully')
    def test_delete_reservation_by_id(self):
        pass
    #     # Connect to the server and send a DELETE request
    #     connection = http.client.HTTPConnection(*self.server_address) 
    #     connection.request('DELETE', '/reservations/1')  # Replace '1' with the desired reservation ID
    #     response = connection.getresponse()

    #     # Read and Decode the response
    #     data = response.read().decode()
    #     connection.close()

    #     # Check that the response is as expected
    #     self.assertEqual(response.status, 200)
    #     self.assertEqual(response.reason, 'OK')
    #     self.assertEqual(response.getheader('Content-Type'), 'application/json')

    #     # Parse the JSON data and verify the content
    #     response_data = json.loads(data)
    #     self.assertEqual(response_data['message'], 'Reservation deleted successfully')

if __name__ == '__main__':
    unittest.main()
