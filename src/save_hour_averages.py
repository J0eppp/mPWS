# Save the averages of files
import json
from os import listdir
from sys import argv

data = {}
averages = {}

def get_average_of_list(arr: list):
    return sum(arr) / len(arr)


def main():
    args = argv[1::]
    if len(args) < 2:
        print('Usage: {} <input_folder> <output_file>'.format(argv[0]))
        exit(-1)

    input_folder = args[0]
    output_file = args[1]
    folder = [x for x in listdir(input_folder) if x.endswith('.json')]
    for file in folder:
        component = file.split('.')[0]
        data[component] = {}
        f = open('{}/{}'.format(input_folder, file), 'r+')
        obj = json.load(f)
        for item in obj:
            if item['timestamp_measured'] in data[component]:
                data[component][item['timestamp_measured']].append(item['value'])
            else:
                data[component][item['timestamp_measured']] = [item['value']]

        for component in data:
            if not component in averages:
                averages[component] = {}
            for timestamp in data[component]:
                averages[component][timestamp] = get_average_of_list(data[component][timestamp])


    f = open(output_file, 'w+')
    json.dump(averages, f, indent = 4)
    f.close()


if __name__ == '__main__':
    main()
