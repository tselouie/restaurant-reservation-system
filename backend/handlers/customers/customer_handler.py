
from db.db_connector import get_customers, insert_customer, get_customer_by_id, update_customer_by_id
import json

def handle_get_customers(request_handler):
    last_parameter = request_handler.path.split("/")[-1]  # Obtain last parameter

    if last_parameter and last_parameter.isdigit():
        customer, error = get_customer_by_id(last_parameter)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        elif customer:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.end_headers()
            response = json.dumps(customer).encode()
        else:
            request_handler.send_response(404)
            request_handler.end_headers()
            response = json.dumps({"error": "Customer not found"}).encode()
    else:
        # Get all records
        records, error = get_customers()
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.end_headers()
            response = json.dumps(records).encode()
    request_handler.wfile.write(response)

def handle_post_customers(request_handler):
    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Assuming 'FirstName' and 'LastName' are required fields for creating a new customer
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    if name is not None and phone is not None:
        customer_id, error = insert_customer(name, email,phone)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.end_headers()
            response = json.dumps({"message": "Customer inserted successfully", "CustomerID": customer_id}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "Name,Email and Phone number are required"}).encode()
    request_handler.wfile.write(response)

def handle_put_customers(request_handler):

    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Extracting fields that might be updated
    customer_id = data.get('customer_id')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    if customer_id is not None and name is not None and email is not None and phone is not None:
        _, error = update_customer_by_id(customer_id,name,email,phone)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.end_headers()
            response = json.dumps({"message": "Customer updated successfully"}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "One of the Fields is missing to update this record."}).encode()
    request_handler.wfile.write(response)

# Logic may not be used as we are not deleting customers

# def handle_delete_customers(request_handler):
#     customer_id = request_handler.path.split("/")[-1] 
#     _, error = delete_customer_by_id(customer_id)
#     if error:
#         request_handler.send_response(500)
#         request_handler.end_headers()
#         response = json.dumps({"error": error}).encode()
#     else:
#         request_handler.send_response(200)
#         request_handler.send_header('Content-type', 'application/json')
#         request_handler.end_headers()
#         response = json.dumps({"message": "Customer deleted successfully"}).encode()
#     request_handler.wfile.write(response)
