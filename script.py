import json
import csv
import os
from datetime import datetime

# List of input file names
file_names = [
    '2022-08.json', 
    '2022-09.json',
    '2022-10.json',
    '2022-11.json',
    '2022-12.json', 
    '2023-01.json',
    '2023-02.json',
    '2023-03.json',
    '2023-04.json',
    '2023-05.json',
    '2023-06.json'
  ]

# Output file name
output_file = 'consolidated_data.csv'

# Open the output file for writing
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['ts', 'datetime', 'key', 'value'])

    # Loop through each input file
    for file_name in file_names:
        with open(file_name) as json_file:
            # Load the JSON data from the file
            data = json.load(json_file)

            # Loop through each key in the JSON data
            for key, values in data.items():
                # Ignore rawData
                if key == 'rawData':
                    continue

                # Loop through each value in the key's list
                for value in values:
                    # Convert the timestamp to a datetime object
                    dt = datetime.fromtimestamp(value['ts'] / 1000)

                    # Write a row to the CSV file
                    writer.writerow([value['ts'], dt.strftime('%Y/%m/%d %H:%M:%S'), key, value['value']])