import csv
import os


def generateAirportInserts(csv_file_path='../data/iata-icao.csv',
                           output_directory_path='../sqlScripts/AirportInserts', maxRowsPerFile=1000):
    readLineCount = 0
    fileIndex = 0
    output_file_path = f"{output_directory_path}/airport_inserts_{fileIndex}.sql"

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Ensure the output directory exists
        os.makedirs(output_directory_path, exist_ok=True)

        output_file = open(output_file_path, mode='w')

        for row in csv_reader:
            name = row['airport'].replace("'", "''")
            latitude = row['latitude']
            longitude = row['longitude']
            iata_code = row['iata']
            icao_code = row['icao']
            if icao_code == '':
                icao_code = 'N/A'
            region_code = row['region_name'].replace("'", "''")

            insert_command = f"INSERT INTO MICHAELBENNIE.Airport (Name, Latitude, Longitude, IATACode, ICAOCode, RegionCode) VALUES ('{name}', {latitude}, {longitude}, '{iata_code}', '{icao_code}', '{region_code}');\n"

            output_file.write(insert_command)
            readLineCount += 1


            #輸出那個文件
            if readLineCount % maxRowsPerFile == 0 and readLineCount:
                output_file.close()
                fileIndex += 1
                output_file_path = f"{output_directory_path}/airport_inserts_{fileIndex}.sql"
                output_file = open(output_file_path, mode='w')

        output_file.close()


def generateAccidentCsv(csv_file_path='../data/US_Accidents_March23.csv',
                        output_file_path='../csvOutputs/Accident.csv'):
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # 確保輸出目錄存在
        output_directory_path = os.path.dirname(output_file_path)
        os.makedirs(output_directory_path, exist_ok=True)

        # 打開輸出文件
        with open(output_file_path, mode='w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            # 寫入列名稱
            csv_writer.writerow(['ID', 'Source', 'Severity', 'DistanceAffected', 'LocStartLatitude', 'LocStartLongitude'])

            for row in csv_reader:
                ID = row['ID']
                Source = row['Source']
                Severity = row['Severity']
                Distance = row['Distance(mi)']
                Start_Lat = row['Start_Lat']
                Start_Lng = row['Start_Lng']

                # 寫入數據行
                csv_writer.writerow([ID, Source, Severity, Distance, Start_Lat, Start_Lng])


def generateTimeCsv(csv_file_path='../data/US_Accidents_March23.csv',
                        output_file_path='../csvOutputs/Time.csv'):
    # 確保輸出目錄存在
    output_directory_path = os.path.dirname(output_file_path)
    os.makedirs(output_directory_path, exist_ok=True)

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        seen_ids = set()

        with open(output_file_path, mode='w', newline='') as output_file:
            fieldnames = ['AccidentID', 'StartTime', 'EndTime', 'TimeZone', 'TimePeriod']
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                accident_id = row['ID']
                # 檢查此條目是否為唯一
                if accident_id not in seen_ids:
                    seen_ids.add(accident_id)
                    csv_writer.writerow({
                        'AccidentID': row['ID'],
                        'StartTime': row['Start_Time'],
                        'EndTime': row['End_Time'],
                        'TimeZone': row['Timezone'],
                        'TimePeriod': row['Sunrise_Sunset']
                    })


def generateWeatherCsv(csv_file_path='../data/US_Accidents_March23.csv',
                        output_file_path='../csvOutputs/Weather.csv'):
    # 確保輸出目錄存在
    output_directory_path = os.path.dirname(output_file_path)
    os.makedirs(output_directory_path, exist_ok=True)

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        seen_ids = set()

        with open(output_file_path, mode='w', newline='') as output_file:
            fieldnames = ['Temperature', 'WindSpeed', 'WeatherCondition', 'Visibility', 'WindDirection', 'Humidity', 'Pressure', 'WindChill','Precipitation',"AccidentID"]
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                accident_id = row['ID']
                # 檢查此條目是否為唯一
                if accident_id not in seen_ids:
                    seen_ids.add(accident_id)
                    csv_writer.writerow({
                        'Temperature': row['Temperature(F)'],
                        'WindSpeed': row['Wind_Speed(mph)'],
                        'WeatherCondition': row['Weather_Condition'],
                        'Visibility': row['Visibility(mi)'],
                        'WindDirection': row['Wind_Direction'],
                        'Humidity': row['Humidity(%)'],
                        'Pressure': row['Pressure(in)'],
                        'WindChill': row['Wind_Chill(F)'],
                        'Precipitation': row['Precipitation(in)'],
                        "AccidentID": row["ID"]
                    })


if __name__ == '__main__':
    #generateAirportInserts()
    #generateAccidentCsv()
    #generateTimeCsv()
    generateWeatherCsv()