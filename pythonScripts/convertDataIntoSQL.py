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


def generateAccidentInserts(csv_file_path='../data/US_Accidents_March23.csv',
                            output_directory_path='../sqlScripts/AccidentInserts', maxRowsPerFile=80000):
    readLineCount = 0
    fileIndex = 0
    output_file_path = f"{output_directory_path}/accident_inserts_{fileIndex}.sql"

    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # 確保輸出目錄存在
        os.makedirs(output_directory_path, exist_ok=True)

        output_file = open(output_file_path, mode='w')

        for i,row in enumerate(csv_reader):
            ID = row['ID']
            Source = row['Source']
            Severity = row['Severity']
            Distance = row['Distance(mi)']
            #The description takes up too much data so we dont include it
            #Description = row['Description'].replace("'", "''")
            Start_Lat = row['Start_Lat']
            Start_Lng = row['Start_Lng']

            insert_command = f"INSERT INTO Accident (ID, Source, Severity, DistanceAffected, LocStartLatitude, LocStartLongitude) VALUES ('{ID}', '{Source}', {Severity}, {Distance}, {Start_Lat}, {Start_Lng});\n"

            output_file.write(insert_command)
            readLineCount += 1

            if readLineCount % maxRowsPerFile == 0 and readLineCount:
                print("row", i)
                output_file.close()
                fileIndex += 1
                output_file_path = f"{output_directory_path}/accident_inserts_{fileIndex}.sql"
                output_file = open(output_file_path, mode='w')

        output_file.close()


if __name__ == '__main__':
    #generateAirportInserts()
    generateAccidentInserts()