# Calculate day averages with hour_averages as an input
import json
from os import listdir
from sys import argv


averages = {}


def get_average_of_list(arr: list):
    return sum(arr) / len(arr)


def main():
    args = argv[1::]
    if len(args) < 2:
        print('Usage: {} <input_file> <output_file>'.format(argv[0]))
        exit(-1)

    input_file = args[0]
    output_file = args[1]

    file = open(input_file, 'r+')
    obj = json.load(file)
    for component in obj:
        if not component in averages:
            averages[component] = {}
        for timestamp in obj[component]:
            date = timestamp.split('T')[0]
            if not date in averages[component]:
                averages[component][date] = [obj[component][timestamp]]
            else:
                averages[component][date].append(obj[component][timestamp])

    for component in averages:
        for date in averages[component]:
            averages[component][date] = get_average_of_list(averages[component][date])

    f = open(output_file, 'w+')
    json.dump(averages, f, indent = 4)


if __name__ == '__main__':
    main()
