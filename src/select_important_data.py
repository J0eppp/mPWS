# Get all the important things from the JSON files
# Written by Joep van Dijk
import json
import sys
from requests import get
from os import listdir
from threading import Thread


threads = []


def do_stuff(input_folder, output_folder, file):
    output = []
    f = open('{}/{}'.format(input_folder, file), 'r+')
    obj = json.load(f)
    for item in obj:
        timestamp = item['timestamp_measured']
        value = item['value']
        station_id = item['station_id']
        output.append({'timestamp': timestamp, 'value': value, 'station_id': station_id})

    output_file = open('{}/{}'.format(output_folder, file), 'w+')
    json.dump(output, output_file, indent = 4)
    output_file.close()
    f.close()


def main():
    args = sys.argv[1::]
    if len(args) < 2:
        print('Usage: {} <input_folder> <output_folder>'.format(sys.argv[0]))
        exit(-1)

    input_folder = args[0]
    output_folder = args[1]
    files_in_input_folder = [file for file in listdir(input_folder) if file.endswith('.json')]
    print(files_in_input_folder)
    for file in files_in_input_folder:
        t = Thread(target = do_stuff, args = (input_folder, output_folder, file))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    main()
