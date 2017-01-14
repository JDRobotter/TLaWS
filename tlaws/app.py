
import threading, signal
import config
from webserver import TlawsWebServer
from logger import TlawsLogger

class TlawsApplication:

    def __init__(self):
        self.not_running = threading.Event()
        print "[+] Starting Tlaws"

        # gracefull shutdown signal handler
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

        # Starting logger
        self.logger = TlawsLogger(self)
        self.logger.start()

        # Starting web server
        self.webserver = TlawsWebServer(self)
        self.webserver.start()

    def shutdown(self, signum, frame):
        print "[-] SIGNAL", signum, "received, shutting down gracefully"
        self.not_running.set()

    def run(self):
        while not self.not_running.is_set():
            self.not_running.wait(1)

        self.webserver.stop()
        self.logger.stop()
        print "[-] Tlaws has stopped"
