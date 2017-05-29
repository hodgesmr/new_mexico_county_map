import csv
import json

INPUT_FILE_PATH = '/Users/hodgesmr/Desktop/trump_income/analysis.csv'
INPUT_2016_RESULTS_PATH = '/Users/hodgesmr/2009_2015_income/2016_county_results.json'
GEO_ID_COLUMN = 0
INCOME_2009_COLUMN = 5
INCOME_2015_COLUMN = 6

trump_count = 0
clinton_count = 0

with open(INPUT_FILE_PATH, 'rb') as input_file:
    reader = csv.reader(input_file)
    header = next(reader)

    income_dict = {}

    for row in reader:
        income_dict[int(row[GEO_ID_COLUMN])] = row

    with open(INPUT_2016_RESULTS_PATH) as results_file:
        results_data = json.load(results_file)

        for geo_id in results_data.keys():
            try:
                income_data = income_dict[int(geo_id)]
                results_data[geo_id]['income_2009'] = int(income_data[INCOME_2009_COLUMN])
                results_data[geo_id]['income_2015'] = int(income_data[INCOME_2015_COLUMN])

                growth = (float((results_data[geo_id]['income_2015']-results_data[geo_id]['income_2009']))/float(results_data[geo_id]['income_2009']))
                if growth < 0:
                    if results_data[geo_id]['trump'] > results_data[geo_id]['clinton']:
                        trump_count += 1
                    elif results_data[geo_id]['clinton'] > results_data[geo_id]['trump']:
                        clinton_count += 1

            except (KeyError, IndexError):
                print('Removing {}'.format(results_data[geo_id]['county']))
                del results_data[geo_id]


        with open('./income_change.json', 'wb') as output_file:
            json.dump(results_data, output_file)

print 'Trump: {}'.format(trump_count)
print 'Clinton: {}'.format(clinton_count)
