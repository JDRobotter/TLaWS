
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
from . import config

class MyHTTPServer(HTTPServer,ThreadingMixIn):
    pass

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/loutre.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open(config.graphs_file_path,'rb').read())

        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ("""<html>
                <body>
                    <h1>
                        hi xxx !
                    </h1>
                    <img src="loutre.png"/>
                </body>
            </html>""")
            self.wfile.write(message.encode())

        else:
            self.send_response(404)
            self.end_headers()


class TlawsWebServer(threading.Thread):
    daemon = True

    def __init__(self, app):
        threading.Thread.__init__(self)
        print("[+] Starting webserver", flush=True)
        self.app = app

        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        if self.running:
            httpd = MyHTTPServer(('', config.port), MyRequestHandler)
            httpd.serve_forever()
        print("[-] Stopping webserver", flush=True)
