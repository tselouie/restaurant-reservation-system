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
import http.client
import json
import threading

class TestServerCustomers(unittest.TestCase):
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
        connection.request('GET', '/customers')
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

    def test_insert_customer(self):
        # Connect to the server and send a POST request to insert a customer record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        customer_data = {'name': 'John Doe', 'email': 'johndoe@example.com','phone': '1234567890'}
        connection.request('POST', '/customers', json.dumps(customer_data), headers)
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
        self.assertEqual(response_data['message'], 'Customer inserted successfully')

    def test_get_customer_by_id(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('GET', '/customers/1')  # Replace '1' with the desired customer ID
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

    def test_update_customer(self):
        # Connect to the server and send a PUT request to update a customer record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        customer_data = {'customer_id': 1, 'name': 'George Doe', 'email': 'georgedoe@example.com','phone': '0987654321'}
        connection.request('PUT', '/customers', json.dumps(customer_data), headers)
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
        self.assertEqual(response_data['message'], 'Customer updated successfully')


if __name__ == '__main__':
    unittest.main()