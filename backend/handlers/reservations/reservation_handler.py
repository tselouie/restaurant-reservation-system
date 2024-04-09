from db.db_connector import get_reservations, insert_reservation, get_reservation_by_id, update_reservation_by_id, delete_reservation_by_id,update_reservation_status
import json
import datetime

# handlers/reservation_handler.py
def handle_get_reservations(request_handler):
    last_parameter = request_handler.path.split("/")[-1]  # Obtain last parameter

    if last_parameter and last_parameter.isdigit() and last_parameter != 'reservations':
        
        reservation, error = get_reservation_by_id(last_parameter)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        elif reservation:
            # Convert datetime object to string representation
            reservation['ReservationDateTime'] = reservation['ReservationDateTime'].isoformat()

            request_handler.send_response(200)
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps(reservation).encode()
        else:
            request_handler.send_response(404)
            request_handler.end_headers()
            response = json.dumps({"error": "Reservation not found"}).encode()
    else:
        # Get all records
        records, error = get_reservations()
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            # Convert datetime objects to string representations
            for record in records:
                record['ReservationDateTime'] = record['ReservationDateTime'].isoformat()
            request_handler.send_response(200)
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps(records).encode()
    request_handler.wfile.write(response)

def handle_post_reservations(request_handler):
    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Assuming 'ReservationName' and 'Date' are required fields for creating a new reservation
    customer_id = data.get('customer_id')
    table_id = data.get('table_id')
    reservation_datetime = data.get('date_time')
    number_of_guests = data.get('guests')
    if customer_id is not None and table_id is not None and reservation_datetime is not None and number_of_guests is not None:
        reservation_id, error = insert_reservation(customer_id,table_id, reservation_datetime,number_of_guests)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps({"message": "Reservation inserted successfully", "ReservationID": reservation_id}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "ReservationName and Date are required"}).encode()
    request_handler.wfile.write(response)

def handle_put_reservations(request_handler):
    content_length = int(request_handler.headers['Content-Length'])
    post_data = request_handler.rfile.read(content_length)
    data = json.loads(post_data.decode('utf-8'))

    # Extracting fields that might be updated
    reservation_id = data.get('reservation_id')
    date_time = data.get('date_time')
    guests = data.get('guests')
    status = data.get('status')
    
    
    if reservation_id is not None and date_time is not None and guests is not None:
        _, error = update_reservation_by_id(reservation_id, date_time, guests)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps({"message": "Reservation updated successfully"}).encode()
    elif status is not None:
        _, error = update_reservation_status(reservation_id, status)
        if error:
            request_handler.send_response(500)
            request_handler.end_headers()
            response = json.dumps({"error": error}).encode()
        else:
            request_handler.send_response(200)
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            request_handler.send_header('Content-type', 'application/json')
            request_handler.end_headers()
            response = json.dumps({"message": "Reservation status updated successfully"}).encode()
    else:
        request_handler.send_response(400)
        request_handler.end_headers()
        response = json.dumps({"error": "ReservationName and Date are required for update"}).encode()
    request_handler.wfile.write(response)

def handle_delete_reservations(request_handler):
    reservation_id = request_handler.path.split("/")[-1]  # Assuming URL pattern is /reservations/<ReservationID>
    _, error = delete_reservation_by_id(reservation_id)
    if error:
        request_handler.send_response(500)
        request_handler.end_headers()
        response = json.dumps({"error": error}).encode()
    else:
        request_handler.send_response(200)
        request_handler.send_header('Access-Control-Allow-Origin', '*')
        request_handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        request_handler.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        request_handler.send_header('Content-type', 'application/json')
        request_handler.end_headers()
        response = json.dumps({"message": "Reservation deleted successfully"}).encode()
    request_handler.wfile.write(response)
