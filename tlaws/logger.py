
import  os, time
import threading
import subprocess
import config

class TlawsLogger(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        print "[+] Starting logger"

        self.app = app
        self.running = True

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
            temp = self.fetch_temp()
            self.log()
            time.sleep(5)
        print "[-] Stopping logger"

