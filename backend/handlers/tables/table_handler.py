# handlers/tables_handler.py
from db.db_connector import get_tables, insert_table, get_table_by_id,update_table_by_id,delete_table_by_id
import json

def handle_get_tables(request_handler):
    last_parameter = request_handler.path.split("/")[-1]  # Obtain last parameter

    if last_parameter and last_parameter.isdigit() and last_parameter != 'tables':
        table, error = get_table_by_id(last_parameter)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        elif table:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps(table).encode()
        else:
            request_handler.send_response(404)
            request_handler.end_headers()
            response = json.dumps({"error": "Table not found"}).encode()
    else:
        # Get all records
        records, error = get_tables()
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps(records).encode()
    request_handler.wfile.write(response)

def handle_post_tables(request_handler):
    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Assuming 'TableNumber' and 'Capacity' are required fields for creating a new table
    table_number = data.get('table_number')
    capacity = data.get('capacity')
    if table_number is not None and capacity is not None:
        table_id, error = insert_table(table_number, capacity)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps({"message": "Table inserted successfully", "TableID": table_id}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "TableNumber and Capacity are required"}).encode()
    request_handler.wfile.write(response)

def handle_put_tables(request_handler):
    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Extracting fields that might be updated
    table_number = data.get('table_number')
    capacity = data.get('capacity')
    table_id = data.get('table_id')
    if table_id is not None and table_number is not None and capacity is not None:
        _, error = update_table_by_id(table_id, table_number, capacity)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps({"message": "Table updated successfully"}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "TableNumber and Capacity are required for update"}).encode()
    request_handler.wfile.write(response)

def handle_delete_tables(request_handler):
    table_id = request_handler.path.split("/")[-1]  # Assuming URL pattern is /tables/<TableID>
    _, error = delete_table_by_id(table_id)
    if error:
        request_handler.send_response(500)
        request_handler.end_headers()
        response = json.dumps({"error": error}).encode()
    else:
        request_handler.send_response(200)
        request_handler.send_header('Content-type', 'application/json')
        request_handler.end_headers()
        response = json.dumps({"message": "Table deleted successfully"}).encode()
    request_handler.wfile.write(response)