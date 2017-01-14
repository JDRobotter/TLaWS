
import  os, time
import threading
from . import config
import rrdtool

class TlawsGrapher(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        print("[+] Starting grapher module", flush=True)

        self.app = app
        self.running = True

        self.day = 86400
        self.week = self.day * 7

        self.ts = time.time()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if time.time() - self.ts > 15:
                rrdtool.graph(config.graphs_file_path,
                    '--start', '-%i' %(2 * self.day),
                    '-a', 'PNG', '-w', '1000', '-h', '500', '-A', '-E',
                    '-y', '1:2', '-n', 'DEFAULT:20', '-n', 'TITLE:30',
                    '-n', 'WATERMARK:1',
                    '--x-grid', 'HOUR:6:DAY:1:DAY:1:86400:%a',
                    '--vertical-label', 'Temperature (degC)',
                    '--title', 'Temperature', '--border', '0',
                    '--color=CANVAS#505050', '--color=BACK#FFFFFF',
                    'DEF:raw_int=%s:int_temp:AVERAGE' % config.rrd_file_path,
                    'CDEF:temp_int=raw_int,UN,0,raw_int,IF',
                    'LINE3:temp_int#FF0000')
                self.ts = time.time()
            time.sleep(1)
        print("[-] Stopping grapher module", flush=True)
