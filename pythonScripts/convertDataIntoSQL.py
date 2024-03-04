import csv


def generateAirportInserts(csv_file_path = '../data/iata-icao.csv', output_file_path = '../sqlScrips/generateAirportInserts.sql'):
    with open(csv_file_path, mode='r') as csv_file, open(output_file_path, mode='w') as output_file:
        # 创建一个csv阅读器对象
        csv_reader = csv.DictReader(csv_file)

        # 遍历CSV文件中的每一行
        for row in csv_reader:
            # 从行中提取各个字段
            name = row['airport'].replace("'", "''")  # 处理名字中的单引号
            latitude = row['latitude']
            longitude = row['longitude']
            iata_code = row['iata']
            icao_code = row['icao']
            if icao_code == '':
                icao_code = 'N/A'
            region_code = row['region_name'].replace("'", "''")  # 处理地区名中的单引号

            # 创建INSERT命令
            insert_command = f"INSERT INTO Airport (Name, Latitude, Longitude, IATACode, ICAOCode, RegionCode) VALUES ('{name}', {latitude}, {longitude}, '{iata_code}', '{icao_code}', '{region_code}');\n"

            # 将INSERT命令写入输出文件
            output_file.write(insert_command)


if __name__ == '__main__':
    generateAirportInserts()