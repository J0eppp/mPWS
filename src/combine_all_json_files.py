# Get all the files from '../data/' and sort them in the four components
# Save everything in 4 big files
# Written by Joep van Dijk
import json
import sys
from os import listdir

data_sorted = {
	'NO': [],
	'NO2': [],
	'PM10': [],
	'PM2.5': []
}

def load_data(folder: str):
	files = [file for file in listdir(folder) if file.endswith('.json')]

	filenames_sorted = {
		'NO': [],
		'NO2': [],
		'PM10': [],
		'PM2.5': []
	}

	for file in files:
		component = file.split('_')[0]
		filenames_sorted[component].append(file)

	return filenames_sorted


def main():
	if len(sys.argv) < 2:
		print('Usage: {} <input_folder> <output_folder>'.format(sys.argv[0]))
		exit(-1)
	input_folder = sys.argv[1]
	output_folder = sys.argv[2]
	filenames_sorted = load_data(input_folder)
	for component in filenames_sorted:
		for filename in filenames_sorted[component]:
			f = open(input_folder + '/' + filename, 'r+')
			obj = json.load(f)
			f.close()
			[data_sorted[component].append(x) for x in obj]

	for component in data_sorted:
		data = data_sorted[component]
		f = open('{}/{}.json'.format(output_folder, component), 'w+')
		json.dump(data, f, indent = 4)
		f.close()



if __name__ == '__main__':
	main()
