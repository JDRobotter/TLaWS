import os

root_folder = '/opt/tlaws/'

rrd_file_path = os.path.join(root_folder, 'rrdtool/temperature.rrd')
temp_file_path = os.path.join(root_folder, 'tlaws/get_temp.out')
graphs_file_path = os.path.join(root_folder, 'graphs/temp.png')

port = 51640
