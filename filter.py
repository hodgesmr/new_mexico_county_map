import copy
import json

INPUT_FILE_PATH = '/Users/hodgesmr/new_mexico_counties/counties.json'
KEY_FILE = '/Users/hodgesmr/new_mexico_counties/2016_county_results.json'
OUTPUT_FILE_PATH = '/Users/hodgesmr/new_mexico_counties/new_mexico_counties.json'

new_mexico_county_ids = set()

with open(KEY_FILE) as all_counties_file:
    all_counties = json.load(all_counties_file)
    for county_id, county_data in all_counties.iteritems():
        if all_counties[county_id]['state'] == 'NM':
            new_mexico_county_ids.add(int(county_id))

with open(INPUT_FILE_PATH) as all_geography_file:
    all_geography = json.load(all_geography_file)

    output_dict = copy.deepcopy(all_geography)
    del output_dict['objects']['states']
    del output_dict['objects']['land']
    output_dict['objects']['counties']['geometries'] = []

    for county in all_geography['objects']['counties']['geometries']:
        county_id = county['id']
        if county_id in new_mexico_county_ids:
            output_dict['objects']['counties']['geometries'].append(county)

    del output_dict['objects']['counties']['bbox']

    with open(OUTPUT_FILE_PATH, 'w') as outfile:
        json.dump(output_dict, outfile)
