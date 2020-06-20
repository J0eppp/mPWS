# This file combines all the other files into one program, easier to do everything :D

import requests, datetime, calendar, json, math, threading, sys, os

components = {  # Stikstofdioxide, Stikstofmonoxide, Fijn stof (PM10), Fijn stof (PM2.5)
    'NO2': '88afd3d1-6da3-496a-ac81-669a47256d34',
    'NO': '32d85dc5-83c3-4d3a-9d76-ccbfbf6f5b61',
    'PM10': 'd28b1762-5179-46da-a90f-cf1d4966ea50',
    'PM2.5': '311aa322-65bf-4f53-9341-702376f437e0'
}

components_reversed = {
    '88afd3d1-6da3-496a-ac81-669a47256d34': 'NO2',
    '32d85dc5-83c3-4d3a-9d76-ccbfbf6f5b61': 'NO',
    'd28b1762-5179-46da-a90f-cf1d4966ea50': 'PM10',
    '311aa322-65bf-4f53-9341-702376f437e0': 'PM2.5'
}

provinces_data = {
    'Drenthe': '1721de96-857b-4cff-ae42-b6be73a27da0',
    'Flevoland': 'f2152205-8585-4cb5-a181-c845ec85439f',
    'Friesland': '71fb022f-2ef3-4f38-b425-a7ff57d7c43f',
    'Gelderland': 'bf9e5fb3-748f-4fdb-a630-1dea22e0f861',
    'Groningen': '1ca9a43e-bd9c-4fc2-aa47-03ec874bfad9',
    'Limburg': 'ea59dc39-4ac2-4e2d-b9dd-2db74d4063bc',
    'Noord-Brabant': '1403bdaa-fb92-412a-a47b-5d76055c596d',
    'Noord-Holland': '4a8fec5e-c1d3-49f3-84a3-28be30ae005e',
    'Overijssel': 'b050c621-ba15-4a8c-8a1c-f0f90fadbef0',
    'Utrecht': '010231f0-dcf7-4c1f-bba1-d31ec66ebbae',
    'Zeeland': '587afa5d-843f-4237-9cbe-21d92eea3375',
    'Zuid-Holland': '5e4d8ed0-de01-49db-8dc1-d01b738c05e1'
}

periods = []

total_requests = 0
requests_done = 0


class Province(threading.Thread):
    def __init__(self, name, id):
        super().__init__()

        self.name = name
        self.id = id
        self.stations = []

        self.start()

    def run(self):
        req = requests.get('https://api2020.luchtmeetnet.nl/stations?show_website=true&limit=999&province_id={}'.format(self.id))
        obj = json.loads(req.text)
        result = obj['result']
        for s in result:
            station_name = s['name']
            station_id = s['id']
            station_location = s['geometry']
            self.stations.append(Station(station_name, station_id, station_location, self))

        for station in self.stations:
            station.join()


class Station(threading.Thread):
    def __init__(self, name: str, id: int, location: list, province: Province):
        super().__init__()
        self.name = name
        self.id = id
        self.location = location
        self.province = province

        global total_requests

        self.total_requests = len(periods) * len(components)
        self.requests_done = 0
        total_requests += self.total_requests

        self.start()

    def run(self):
        # https://api2020.luchtmeetnet.nl/measurements?component_id={component_id}&start={start}&end={end}&station_id={station_id}&limit=999&zero_fill=1&order_direction=asc&status=validated,unvalidated
        for period in periods:
            start = period[0]
            end = period[1]
            for component in components:
                component_id = components[component]
                url = 'https://api2020.luchtmeetnet.nl/measurements?component_id={component_id}&start={start}&end={end}&station_id={station_id}&limit=999&zero_fill=1&order_direction=asc&status=validated,unvalidated'.format(component_id = component_id, start = start, end = end, station_id = self.id)
                if len(sys.argv) >= 6:
                    url = 'https://api2020.luchtmeetnet.nl/measurements?component_id={component_id}&start={start}&end={end}&station_id={station_id}&limit=999&zero_fill=1&order_direction=asc&status={status}'.format(component_id = component_id, start = start, end = end, station_id = self.id, status = sys.argv[5])
                try:
                    result = json.loads(requests.get(url).text)['result']
                    self.requests_done += 1
                    global requests_done
                    requests_done += 1
                    if len(result) == 0:
                        # log('Skipped this file: {}'.format('../data/{}_{}_{}_{}.json'.format(component, self.id, start.replace(':', ';'), end.replace(':', ';'))))
                        # log(url)
                        continue
                    else:
                        # Save the data here
                        file = open('../data/{}_{}_{}_{}.json'.format(component, self.id, start.replace(':', ';'), end.replace(':', ';')), 'w+')
                        json.dump(result, file, indent = 4)
                        file.close()
                except requests.exceptions.SSLError:
                        self.requests_done += 1
                        requests_done += 1
                        # log('SSL Exception on file: {}'.format('../data/{}_{}_{}_{}.json'.format(component, self.id, start.replace(':', ';'), end.replace(':', ';'))))


def get_periods_of_month(year: int, month: int):
    cal = calendar.Calendar(0)
    month_list = cal.monthdays2calendar(year, month)
    for i in range(len(month_list)):
        for j in range(len(month_list[i])):
            if month_list[i][j][0] == 0: month_list[i][j] = None

        month_list[i] = [x for x in month_list[i] if x]

    ret = []

    for week in month_list:
        start_day = week[0][0]
        end_day = week[-1][0]
        start_date = datetime.datetime(year, month, start_day)
        end_date = datetime.datetime(year, month, end_day)
        start_date_arr = str(start_date).split(' ')
        start_date = start_date_arr[0] + 'T' + start_date_arr[1] + '+02'
        end_date_arr = str(end_date).split(' ')
        time_array = end_date_arr[1].split(':')
        time_array[0] = '23'
        time_array[1] = '59'
        time_array[2] = '59'
        end_date_arr[1] = '{}:{}:{}'.format(time_array[0], time_array[1], time_array[2])
        end_date = end_date_arr[0] + 'T' + end_date_arr[1] + '+02'
        ret.append([str(start_date), str(end_date)])

    return ret


def get_data_from_luchtmeetnet_info():
    progressbar_width = 100
    while True:
        if total_requests == 0: continue
        percentage_done = requests_done / (total_requests) * 100
        print("[{}] {}%, {}/{}  ".format("#" * round(percentage_done) + "." * (100 - round(percentage_done)), round(percentage_done, 2), requests_done, total_requests), end = '\r')

        if requests_done == total_requests:
            print("[{}] {}%, {}/{}  ".format("#" * 100, 100, requests_done, total_requests))
            break


def get_data_from_luchtmeetnet():
    p = get_periods_of_month(2019, 4)
    for week in p:
        periods.append(week)
    p = get_periods_of_month(2020, 4)
    for week in p:
        periods.append(week)


    provinces = []
    for province in provinces_data:
        provinces.append(Province(province, provinces_data[province]))

    info_thread = threading.Thread(target = get_data_from_luchtmeetnet_info)
    info_thread.start()

    for province in provinces:
        province.join()

    info_thread.join()


# Combine all the files into 4 big files
data_sorted = {
	'NO': [],
	'NO2': [],
	'PM10': [],
	'PM2.5': []
}

def combine_files_load_data(folder: str):
	files = [file for file in os.listdir(folder) if file.endswith('.json')]

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

def combine_files(input_folder, output_folder):
    # if len(sys.argv) < 2:
	# 	print('Usage: {} <input_folder> <output_folder>'.format(sys.argv[0]))
	# 	exit(-1)
	# input_folder = sys.argv[1]
	# output_folder = sys.argv[2]
	filenames_sorted = combine_files_load_data(input_folder)
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

# Select all the data that we actually need
threads = []


def select_important_data_stuff(input_folder, output_folder, file):
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

def select_important_data(input_folder, output_folder):
    # rgs = sys.argv[1::]
    # if len(args) < 2:
    #     print('Usage: {} <input_folder> <output_folder>'.format(sys.argv[0]))
    #     exit(-1)
    #
    # input_folder = args[0]
    # output_folder = args[1]
    files_in_input_folder = [file for file in os.listdir(input_folder) if file.endswith('.json')]
    print(files_in_input_folder)
    for file in files_in_input_folder:
        t = threading.Thread(target = select_important_data_stuff, args = (input_folder, output_folder, file))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def main():
    combine_input = sys.argv[1]
    combine_output = sys.argv[2]
    select_input = sys.argv[3]
    select_output = sys.argv[4]
    get_data_from_luchtmeetnet()
    combine_files(combine_input, combine_output)
    select_important_data(select_input, select_output)


if __name__ == '__main__':
    main()
