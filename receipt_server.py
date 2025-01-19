from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from Models.receipt import Receipt

receipt_store = {}
class ReceiptHandler(BaseHTTPRequestHandler):
    def set_response(self, code, response):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        if self.path == "/receipts/process":
            content_length = int(self.headers.get('content-length'))
            post_data = self.rfile.read(content_length)
            try:
                receipt_json = json.loads(post_data.decode())
                receipt = Receipt(receipt_json)
                receipt_store[receipt.id] = receipt
                response = {'id': receipt.id}
                self.set_response(200, response)
            except Exception as e:
                response = {'BadRequest': 'The receipt is invalid'}
                self.set_response(400, response)



        else:
            self.my_response(400, b'Bad Request')

    def do_GET(self):
        if self.path == "/receipts/points":
            self.my_response(200, b'GET Request Received!') 
        else:
            self.my_response(404, b'Not Found')

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ReceiptHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()