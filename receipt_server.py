from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
from Models.receipt import Receipt

# In-memory data store to store purchase receipts.
receipt_store = {}

class ReceiptHandler(BaseHTTPRequestHandler):
    """
    A request handler for the Receipt Processor.
    Handles HTTP requests for processing purchase receipts.

    Supported endpoints:
    - POST /receipts/process: Processes and stores a receipt.
    - GET /receipts/{id}/points: Retrieves reward points for the receipt.
    """
    def set_response(self, code, response):
        """
        A wrapper function to send a response to the client.

        Args:
            code (int): The HTTP status code to be returned.
            response (dict): The response body to be returned.
        """

        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """
        Handles POST requests for processing purchase receipts.
        
        Endpoint:
            /receipts/process
        
        Expected Request Body:
            JSON object containing receipt details.
        
        Response:
            200 OK: If receipt data is valid, returns the ID assigned to the receipt.
            400 Bad Request: If the receipt data is invalid.
        """
        if self.path == "/receipts/process":
            content_length = int(self.headers.get('content-length'))
            post_data = self.rfile.read(content_length)
            try:
                receipt_data = json.loads(post_data.decode())
                receipt = Receipt(receipt_data)
                receipt_id = receipt.getId()
                receipt_store[receipt_id] = receipt
                response = {'id': receipt_id}
                self.set_response(200, response)
            except Exception as e:
                response = {'error': 'The receipt is invalid.'}
                self.set_response(400, response)
        else:
            response = {'error': 'Not found.'}
            self.set_response(404, response)

    def do_GET(self):
        """
        Handles GET requests to retrieve receipt points awarded.
        
        Endpoint:
            /receipts/{id}/points
        
        Response:
            200 OK: If valid ID, returns the points associated with the given receipt ID.
            404 Not Found: If the receipt ID does not exist.
        """
        if re.match(r'^/receipts/[^/]+/points$', self.path):
            receipt_id = self.path.split('/')[2]
            try:
                assert re.match(r'^\S+$', receipt_id)
                assert receipt_id in receipt_store
                points = receipt_store[receipt_id].getPoints()
                response = {'points': points}
                self.set_response(200, response)
            except Exception as e:
                response = {'error': 'No receipt found for that ID.'}
                self.set_response(404, response)
        else:
            response = {'error': 'Not found.'}
            self.set_response(404, response)

if __name__ == "__main__":
    server_address = ('', 8000) # Hosted on localhost:8000
    httpd = HTTPServer(server_address, ReceiptHandler)
    print('Starting server on http://localhost:8000')
    httpd.serve_forever()