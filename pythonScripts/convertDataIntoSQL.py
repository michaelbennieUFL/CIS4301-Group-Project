import csv
import os


def generateAirportInserts(csv_file_path='../data/iata-icao.csv',
                           output_directory_path='../sqlScripts/AirportInserts', maxRowsPerFile=1000):
    readLineCount = 0
    fileIndex = 0
    output_file_path = f"{output_directory_path}/airport_inserts_{fileIndex}.sql"

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # 確保輸出目錄存在
        os.makedirs(output_directory_path, exist_ok=True)

        output_file = open(output_file_path, mode='w')

        for row in csv_reader:
            # 將緯度和經度轉換為浮點數
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            # 只有當緯度和經度在美國範圍內時才處理
            if 18.9 <= latitude <= 70 and -165 <= longitude <= -65:
                name = row['airport'].replace("'", "''")
                iata_code = row['iata']
                icao_code = row['icao']
                if icao_code == '':
                    icao_code = 'N/A'
                region_code = row['region_name'].replace("'", "''")

                insert_command = f"INSERT INTO MICHAELBENNIE.Airport (Name, Latitude, Longitude, IATACode, ICAOCode, RegionCode) VALUES ('{name}', {latitude}, {longitude}, '{iata_code}', '{icao_code}', '{region_code}');\n"

                output_file.write(insert_command)
                readLineCount += 1

                # 當達到最大行數限制時，開始寫入新的檔案
                if readLineCount % maxRowsPerFile == 0 and readLineCount:
                    output_file.close()
                    fileIndex += 1
                    output_file_path = f"{output_directory_path}/airport_inserts_{fileIndex}.sql"
                    output_file = open(output_file_path, mode='w')

        output_file.close()


def generateAccidentCsv(csv_file_path='../data/US_Accidents_March23.csv',
                        output_file_path='../csvOutputs/Accident.csv',
                        include_ratio=(3, 5)):  # include_percent參數控制包括的行比例
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # 確保輸出目錄存在
        output_directory_path = os.path.dirname(output_file_path)
        os.makedirs(output_directory_path, exist_ok=True)

        with open(output_file_path, mode='w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            # 寫入列名稱
            csv_writer.writerow(
                ['ID', 'Severity', 'DistanceAffected', 'LocStartLatitude', 'LocStartLongitude', 'EndLatitude',
                 'EndLongitude'])

            row_counter = 0
            for row in csv_reader:
                # 根據指定的百分比跳過行
                if row_counter % include_ratio[1] >= include_ratio[1] - include_ratio[0]:
                    ID = row['ID'][2:]
                    Severity = row['Severity']
                    Distance = row['Distance(mi)']
                    Start_Lat = row['Start_Lat']
                    Start_Lng = row['Start_Lng']
                    End_Lat = row['End_Lat']
                    End_Lng = row['End_Lng']

                    # 寫入數據行
                    csv_writer.writerow([ID, Severity, Distance, Start_Lat, Start_Lng, End_Lat, End_Lng])
                row_counter += 1


def generateTimeCsv(csv_file_path='../data/US_Accidents_March23.csv',
                    output_file_path='../csvOutputs/Time.csv',
                    include_ratio=(3, 5)):
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
            row_counter = 0

            for row in csv_reader:
                accident_id = row['ID'][2:]
                # 檢查此條目是否為唯一
                if accident_id not in seen_ids:
                    if row_counter % include_ratio[1] >= include_ratio[1] - include_ratio[0]:
                        seen_ids.add(accident_id)
                        csv_writer.writerow({
                            'AccidentID': accident_id,
                            'StartTime': row['Start_Time'],
                            'EndTime': row['End_Time'],
                            'TimeZone': row['Timezone'],
                            'TimePeriod': (row['Sunrise_Sunset'] == 'Day') * 1
                        })
                row_counter += 1


def generateWeatherCsv(csv_file_path='../data/US_Accidents_March23.csv',
                       output_file_path='../csvOutputs/Weather.csv',
                       include_ratio=(3, 5)):
    # 確保輸出目錄存在
    output_directory_path = os.path.dirname(output_file_path)
    os.makedirs(output_directory_path, exist_ok=True)

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        seen_ids = set()

        with open(output_file_path, mode='w', newline='') as output_file:
            fieldnames = ['Temperature', 'WindSpeed', 'WeatherCondition', 'Visibility', 'WindDirection', 'Humidity',
                          'Pressure', 'WindChill', 'Precipitation', "AccidentID"]
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            row_counter = 0

            for row in csv_reader:
                accident_id = row['ID'][2:]
                # 檢查此條目是否為唯一
                if accident_id not in seen_ids:
                    if row_counter % include_ratio[1] >= include_ratio[1] - include_ratio[0]:
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
                            "AccidentID": accident_id
                        })
                row_counter += 1


def generateRoadConditionCsv(csv_file_path='../data/US_Accidents_March23.csv',
                             output_file_path='../csvOutputs/RoadCondition.csv',
                             include_ratio=(3, 5)):
    # 確保輸出目錄存在
    output_directory_path = os.path.dirname(output_file_path)
    os.makedirs(output_directory_path, exist_ok=True)

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        seen_locations = set()
        row_counter = 0
        number_of_repetitions = 0
        with open(output_file_path, mode='w', newline='') as output_file:
            fieldnames = ['Bump', 'Amenity', 'NoExit', 'TrafficSignal', 'Railway', 'TrafficCalming', 'GiveWay',
                          'TurningLoop', "Roundabout", 'Crossing', 'Station', 'Stop', "Junction", 'LocStartLatitude',
                          'LocStartLongitude']
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                if row_counter % include_ratio[1] >= include_ratio[1] - include_ratio[0]:
                    location = (row['Start_Lat'], row['Start_Lng'])
                    # 檢查此條目是否為唯一
                    if location not in seen_locations:
                        seen_locations.add(location)
                        csv_writer.writerow({
                            'Bump': (row['Bump'] == "True") * 1,
                            'Amenity': (row['Amenity'] == "True") * 1,
                            'NoExit': (row['No_Exit'] == "True") * 1,
                            'TrafficSignal': (row['Traffic_Signal'] == "True") * 1,
                            'Railway': (row['Railway'] == "True") * 1,
                            'TrafficCalming': (row['Traffic_Calming'] == "True") * 1,
                            'GiveWay': (row['Give_Way'] == "True") * 1,
                            'TurningLoop': (row['Turning_Loop'] == "True") * 1,
                            'Roundabout': (row['Roundabout'] == "True") * 1,
                            'Crossing': (row['Crossing'] == "True") * 1,
                            'Station': (row['Station'] == "True") * 1,
                            'Stop': (row['Stop'] == "True") * 1,
                            'Junction': (row['Junction'] == "True") * 1,
                            'LocStartLatitude': row['Start_Lat'],
                            'LocStartLongitude': row['Start_Lng'],
                        })
                    else:
                        number_of_repetitions += 1
                row_counter += 1
        print("repition ratio: " + str(number_of_repetitions / row_counter))


def generateLocationCsv(csv_file_path='../data/US_Accidents_March23.csv',
                        output_file_path='../csvOutputs/Location.csv',
                        include_ratio=(3, 5)):
    # 確保輸出目錄存在
    output_directory_path = os.path.dirname(output_file_path)
    os.makedirs(output_directory_path, exist_ok=True)

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        seen_locations = set()

        with open(output_file_path, mode='w', newline='') as output_file:
            fieldnames = ['AirportCode', 'Street', 'City', 'Zipcode', 'County', 'State', 'Country',
                          'StartLatitude', 'StartLongitude', 'AirportICAOCode']
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            row_counter = 0
            number_of_repetitions = 0
            for row in csv_reader:
                # 使用起始和結束經緯度作為唯一標識符的一部分
                location_key = (row['Start_Lat'], row['Start_Lng'])
                if row_counter % include_ratio[1] >= include_ratio[1] - include_ratio[0]:
                    if location_key not in seen_locations:
                        seen_locations.add(location_key)
                        csv_writer.writerow({
                            'Street': row.get('Street', None),
                            'City': row.get('City', None),
                            'Zipcode': row.get('Zipcode', None),
                            'State': row.get('State', None),
                            'StartLatitude': row['Start_Lat'],
                            'StartLongitude': row['Start_Lng'],
                            'AirportICAOCode': row['Airport_Code']  # 假設值，根據實際情況替換
                        })
                    else:
                        number_of_repetitions += 1
                row_counter += 1
            print("repetition ratio: " + str(number_of_repetitions / row_counter))


if __name__ == '__main__':
    #generateAirportInserts()
    generateAccidentCsv()
    generateTimeCsv()
    generateWeatherCsv()
    generateRoadConditionCsv()
    generateLocationCsv()
