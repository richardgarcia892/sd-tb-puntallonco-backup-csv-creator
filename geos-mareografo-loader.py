# GEOS MAREOGRAFO LOADER
# Script para cargar el historico en GEOS del dispositivo mareografo.
import csv
import requests
from datetime import datetime, timezone, timedelta

csv_file_path = 'data-output/tb-est06-historico.csv'
api_ednpoint = 'https://zrepo.geoos.org/dataSet/rie.huinay-sd?token=rie-smartd-token'


def get_timestamp_millis(telemetry_date_time):
    # Function to get miliseconds timestamp from date string
    # Get Timezone offset from Venezuela (UTC -4:00)
    timezone_offset = timedelta(hours=-4)
    # Convert telemetry_date_time to UTC and apply offset
    telemetry_utc_time = telemetry_date_time - timezone_offset
    # Convert from date to timestamp (milliseconds)
    telemetry_timestamp_ms = int(telemetry_utc_time.timestamp() * 1000)
    return telemetry_timestamp_ms


def create_mareografo_payload(telemetry):
    # function to create the API payload.
    # Get date time as object
    date_time = datetime.strptime(telemetry[0], '%Y-%m-%d %H:%M:%S')

    # Calculate milliseconds timestamp
    timestamp_ms = get_timestamp_millis(date_time)

    # Get telemetries readigs
    battery = telemetry[1]
    sea_level = telemetry[2]

    # Create payload Object
    payload = {
        'codigoEstacion': 'mareo-sd-001',
        'timestamp': timestamp_ms,
    }

    # add readings (if exist)
    if battery:
        payload['battery'] = float(battery)

    if sea_level:
        payload['nivelMar'] = float(sea_level)

    return payload


# Open CSV File
with open(csv_file_path, newline='') as csvfile:
    # Create CSV reader object
    reader = csv.reader(csvfile, delimiter=';')

    # Get the total number of rows
    telemetry_count = sum(1 for row in reader)
    print(f"Total number of Telemetry to upload: {telemetry_count}")

    # Reset the file pointer to the beginning of the file
    csvfile.seek(0)

    # Skip the headers
    next(reader)

    for telemetry_index, telemetry in enumerate(reader):
        print(f"Telemetry Index: {telemetry_index + 1}/{telemetry_count}")

        # Create payload for mareografo
        payload = create_mareografo_payload(telemetry)

        # Perform HTTP REQUEST to GEOS API.
        response = requests.post(api_ednpoint, json=payload)
        print(response.status_code)
