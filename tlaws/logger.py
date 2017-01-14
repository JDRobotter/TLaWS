
import  os, time
import threading
import subprocess
from . import config

class TlawsLogger(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        print("[+] Starting logger module", flush=True)

        self.app = app
        self.running = True

        self.ts = time.time()

    def fetch_temp(self):
        self.temp =  float(subprocess.Popen([config.temp_file_path],
            stdout=subprocess.PIPE).communicate()[0])

    def log(self):
        os.system("rrdtool update %s N:%f"%(config.rrd_file_path,
            self.temp))

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if time.time() - self.ts > 5:
                temp = self.fetch_temp()
                self.log()
                self.ts = time.time()
            time.sleep(1)
        print("[-] Stopping logger module", flush=True)

