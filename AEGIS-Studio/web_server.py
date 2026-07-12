# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class AegisStudioHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "online",
            "message": "Welcome to AEGIS Studio API",
            "version": "12.0.0-Elite"
        }
        self.wfile.write(json.dumps(response).encode())

def run_studio(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AegisStudioHandler)
    print(f"Starting AEGIS Studio UI Server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    # run_studio() # Uncomment to start server
    print("AEGIS Studio Web Server Module Loaded.")
