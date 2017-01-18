
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
from . import config

import os,sys,json

class MyHTTPServer(HTTPServer,ThreadingMixIn):
    pass

class MyRequestHandler(BaseHTTPRequestHandler):

    def _parse_url(self):
        # parse URL
        path = self.path.strip('/')
        sp = path.split('?')
        if len(sp) == 2:
            path, params = sp
        else:
            path, = sp
            params = None
        args = path.split('/')

        return path,params,args

    def log_message(self, format, *args):
        pass # nothing to do

    def do_GET(self):

        path,params,args = self._parse_url()

#        print(path,params,args)

        if ('..' in args) or ('.' in args):
            self.send_error(400, "A .. ? Really ?")
            self.end_headers()

        if path == '':
            path = 'index.html'

        if path == 'status.json':
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Cache-Control','no-cache, no-store, must-revalidate')
            self.send_header('Pragma','no-cache')
            self.send_header('Expires','0')
            self.end_headers()

            obj = {
                'temperature':self.server.app.logger.temp,
            }

            self.wfile.write(
                json.dumps(obj).encode()
            )
            return

        realpath = os.path.join('www',path)

        if not os.path.isfile(realpath):
            self.send_error(404, "File not found")
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Cache-Control','public, max-age=86400')
        self.end_headers()

 #       print("serving",realpath)
        self.wfile.write(bytes(open(realpath,'rb').read()))

class TlawsWebServer(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        print("[+] Starting webserver", flush=True)
        self.app = app
        self.httpd = None

    def stop(self):
        if self.httpd is not None:
            self.httpd.shutdown()

    def run(self):
        self.httpd = MyHTTPServer(('', config.port), MyRequestHandler)
        self.httpd.app = self.app
        self.httpd.serve_forever()
        print("[-] Stopping webserver", flush=True)
