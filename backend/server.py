from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# from dotenv import load_dotenv
# import os
import mysql.connector
from db.connect import db_connection
from db.db_setup import db_init

import sys
from pathlib import Path

from urllib.parse import urlparse, parse_qs
from handlers.tables.table_handler import handle_get_tables, handle_post_tables, handle_put_tables, handle_delete_tables
from handlers.customers.customer_handler import handle_get_customers, handle_post_customers, handle_put_customers
from handlers.reservations.reservation_handler import handle_get_reservations, handle_post_reservations, handle_put_reservations, handle_delete_reservations
from datetime import date, datetime
import bcrypt

# load_dotenv()  # take environment variables from .env.

# global variable of the list of tables
table_list = ['tables','customers','reservations']

# Function to parse dates in the JSON response
def parse_dates(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d")  # Customize the format as needed
    elif isinstance(obj, dict):
        return {k: parse_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [parse_dates(item) for item in obj]
    else:
        return obj


class RequestHandler(BaseHTTPRequestHandler):

    # GET METHOD - fetch views from database
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parameters = parse_qs(parsed_path.query)

        # Split path and remove the first empty string
        path_parts = parsed_path.path.split('/')[1:]

        # if there are 2 parameters: (table and user_id) and the parameter is one of our tables
        if path_parts[0] in table_list:
            if path_parts[0] == 'tables':
                handle_get_tables(self)
            elif path_parts[0] == 'customers':
                handle_get_customers(self)
            elif path_parts[0] == 'reservations':
                handle_get_reservations(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        else:
            self.send_error(404, "Resource not found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        parameters = parse_qs(parsed_path.query)

        # Split path and remove the first empty string
        path_parts = parsed_path.path.split('/')[1:]

        # if there are 2 parameters: (table and user_id) and the parameter is one of our tables
        if path_parts[0] in table_list:
            if path_parts[0] == 'tables':
                handle_post_tables(self)
            elif path_parts[0] == 'customers':
                handle_post_customers(self)
            elif path_parts[0] == 'reservations':
                handle_post_reservations(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        else:
            self.send_error(404, "Resource not found")

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        parameters = parse_qs(parsed_path.query)

        # Split path and remove the first empty string
        path_parts = parsed_path.path.split('/')[1:]

        # if there are 2 parameters: (table and user_id) and the parameter is one of our tables
        if path_parts[0] in table_list:
            if path_parts[0] == 'tables':
                handle_put_tables(self)
            elif path_parts[0] == 'customers':
                handle_put_customers(self)
            elif path_parts[0] == 'reservations':
                handle_put_reservations(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        else:
            self.send_error(404, "Resource not found")

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        parameters = parse_qs(parsed_path.query)

        # Split path and remove the first empty string
        path_parts = parsed_path.path.split('/')[1:]

        # if there are 2 parameters: (table and user_id) and the parameter is one of our tables
        if path_parts[0] in table_list:
            if path_parts[0] == 'tables':
                handle_delete_tables(self)
            elif path_parts[0] == 'reservations':
                handle_delete_reservations(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        else:
            self.send_error(404, "Resource not found")


def run(serverClass=HTTPServer, handlerClass=RequestHandler, port=8010):
    db_init()  # create all tables and initial records
    serverAddress = ('', port)
    httpd = HTTPServer(serverAddress, RequestHandler)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping the httpd server..')


if __name__ == '__main__':
    run()