# GEOS MAREOGRAFO LOADER
# Script para cargar el historico en GEOS del dispositivo mareografo.
import csv
import requests

csv_file_path = 'data-output/tb-puntallonco-historico.csv'
api_ednpoint = 'https://zrepo.geoos.org/dataSet/rie.huinay-sd?token=rie-smartd-token'
valid_telemetry_keys = ['temperature', 'humidity',
                        'wind_speed', 'wind_direction', 'precipitation2mm']


def create_mareografo_payload(telemetry):
    # function to create the API payload.
    # Get telemetries readigs
    telemetry_ts = telemetry[0]
    teleketry_key = telemetry[2]
    telemetry_val = telemetry[3]

    # Create payload Object
    payload = {
        'codigoEstacion': 'huinay-sd-punta-llonco',
        'timestamp': telemetry_ts,
    }
    if teleketry_key == 'temperature':
        teleketry_key = 'airTemperature'
    if teleketry_key == 'humidity':
        teleketry_key = 'airHumidity'
    if teleketry_key == 'wind_speed':
        teleketry_key = 'windSpeed'
    if teleketry_key == 'wind_direction':
        teleketry_key = 'windDirection'
    if teleketry_key == 'precipitation2mm':
        teleketry_key = 'precipitation'

    payload[teleketry_key] = float(telemetry_val)

    return payload


# Open CSV File
with open(csv_file_path, newline='') as csvfile:
    # Create CSV reader object
    reader = csv.reader(csvfile, delimiter=',')

    # Get the total number of rows
    telemetry_count = sum(1 for row in reader)
    print(f"Total number of Telemetry to upload: {telemetry_count}")

    # Reset the file pointer to the beginning of the file
    csvfile.seek(0)

    # Skip the headers
    next(reader)

    for telemetry_index, telemetry in enumerate(reader):
        print(f"Telemetry Index: {telemetry_index + 1}/{telemetry_count}")

        if telemetry[2] in valid_telemetry_keys:
            # Create payload for mareografo
            payload = create_mareografo_payload(telemetry)
            # print(payload)

            # Perform HTTP REQUEST to GEOS API.
            response = requests.post(api_ednpoint, json=payload)
            print(response.status_code)
