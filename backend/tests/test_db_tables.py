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

class TestServerTables(unittest.TestCase):
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
        connection.request('GET', '/tables')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
    
    def test_get_available_tables_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('GET', '/tables/available?capacity=4&date=2024-12-21&time=20:30:00')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        print(data)

    def test_insert_table(self):
        # Connect to the server and send a POST request to insert a table record
        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        table_data = {'table_number': 1, 'capacity': 4}
        connection.request('POST', '/tables', json.dumps(table_data), headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data['message'], 'Table inserted successfully')

    def test_get_by_id_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('GET', '/tables/1')  # Replace '1' with the desired table ID
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

    def test_handle_put_tables(self):

        connection = http.client.HTTPConnection(*self.server_address) 
        headers = {'Content-Type': 'application/json'}
        table_data = {'table_id':1,'table_number': 1, 'capacity': 8}
        connection.request('PUT', '/tables', json.dumps(table_data), headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()
        response_data = json.loads(data)
        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        self.assertEqual(response_data['message'], 'Table updated successfully')
  
    def test_delete_table_by_id(self):
        # Connect to the server and send a DELETE request
        connection = http.client.HTTPConnection(*self.server_address) 
        connection.request('DELETE', '/tables/5')  # Replace '1' with the desired table ID
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()
        response_data = json.loads(data)
        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        self.assertEqual(response_data['message'], 'Table deleted successfully')

if __name__ == '__main__':
    unittest.main()