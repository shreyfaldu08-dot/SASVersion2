import http.server
import os
import socketserver
import sys

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        fs_path = super().translate_path(path)
        if not os.path.exists(fs_path) and os.path.exists(fs_path + '.html'):
            return fs_path + '.html'
        if fs_path.endswith(os.sep) and os.path.exists(fs_path[:-1] + '.html'):
            return fs_path[:-1] + '.html'
        return fs_path

def start_server():
    requested_port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    ports_to_try = [requested_port] if requested_port else [3001, 3000, 8080]

    for port in ports_to_try:
        try:
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(("", port), CleanURLHandler)
            print(f"Clean URL Server running at http://localhost:{port}")
            httpd.serve_forever()
            return
        except OSError:
            print(f"Port {port} in use, trying next...")

if __name__ == '__main__':
    start_server()
