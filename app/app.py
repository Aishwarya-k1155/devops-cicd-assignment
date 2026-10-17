
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "message": "Hello! CI/CD pipeline is working.",
            "status": "success"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("0.0.0.0", 5000), AppHandler)
print("Application running on port 5000")
server.serve_forever()

