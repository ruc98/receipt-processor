from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'GET Request Received!')

    def do_POST(self):
        content_length = int(self.headers.get('content-length'))
        message_content = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST Request Received!")
        self.wfile.write(message_content)

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()