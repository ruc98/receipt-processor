from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def my_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message)

    def do_GET(self):
        if self.path == "/receipts/points":
            self.my_response(200, b'GET Request Received!') 
        else:
            self.my_response(404, b'Not Found')


    def do_POST(self):
        if self.path == "/receipts/process":
            content_length = int(self.headers.get('content-length'))
            message_content = self.rfile.read(content_length)
            self.my_response(200, b'POST Request Received: ' + message_content)
        else:
            self.my_response(400, b'Bad Request')

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()