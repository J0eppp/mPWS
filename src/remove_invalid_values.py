import json, sys, os


def main():
	input_folder = sys.argv[1]
	output_folder = sys.argv[2]
	files = [filename for filename in os.listdir(input_folder) if filename.endswith('.json')]

	for file in files:
		f = open('{}/{}'.format(input_folder, file), 'r+')
		obj = json.load(f)
		f.close()
		for i in range(len(obj)):
			x = obj[i]
			if x['value'] == -999:
				obj[i] = None
		
		output = open('{}/{}'.format(output_folder, file), 'w+')
		json.dump(obj, output, indent = 4)
		output.close()

	print("Done!")




if __name__ == '__main__':
	main()
