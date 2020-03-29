import http.server
import socketserver
import webbrowser

from shared import host, port


print("opening browser...")
url = f"http://{host}:{port}"
webbrowser.open(url)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer((host, port), Handler)
print(f"serving at: {host}:{port}")
httpd.serve_forever()