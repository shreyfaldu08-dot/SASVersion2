import http.server
import os
import socketserver

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        fs_path = super().translate_path(path)
        if not os.path.exists(fs_path) and os.path.exists(fs_path + '.html'):
            return fs_path + '.html'
        if fs_path.endswith(os.sep) and os.path.exists(fs_path[:-1] + '.html'):
            return fs_path[:-1] + '.html'
        return fs_path

if __name__ == '__main__':
    PORT = 3000
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Clean URL Server running on port {PORT}")
        httpd.serve_forever()
