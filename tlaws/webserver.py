
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import config

class MyHTTPServer(HTTPServer,ThreadingMixIn):
    pass

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/loutre.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open(config.graphs_file_path,'r').read())

        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("""<html>
                <body>
                    <h1>
                        hi xxx !
                    </h1>
                    <img src="loutre.png"/>
                </body>
            </html>""")

        else:
            self.send_response(404)
            self.end_headers()


class TlawsWebServer(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        print "[+] Starting webserver"
        self.app = app

        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        if self.running:
            print 'running'
            httpd = MyHTTPServer( ('',config.port), MyRequestHandler)
            httpd.serve_forever()
        print "[-] Stopping webserver"
