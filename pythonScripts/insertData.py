import time

import oracledb
from concurrent.futures import ThreadPoolExecutor
import os

# 数据库连接信息
username = 'michaelbennie'
password = 'GOxpdrdXBmxHTC0tfKflZZpB'
dsn = 'oracle.cise.ufl.edu:1521/orcl'


def execute_sql_script(file_path):
    # 连接到数据库
    with oracledb.connect(user=username, password=password, dsn=dsn) as connection:
        # 创建一个新的游标
        cursor = connection.cursor()
        # 打开 SQL 文件并读取 SQL 命令
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.readlines()

        line_counter = 0  #
        start_time = time.time()

        try:
            for line in sql_script:
                line = line.strip().strip(';')
                # 执行 SQL 脚本
                if line:
                    cursor.execute(line)
                    line_counter += 1
                    if line_counter % 1000 == 0:
                        elapsed_time = time.time() - start_time
                        print(f"Executed 1000 lines in {elapsed_time:.2f} seconds")
                        start_time = time.time()  # 重置开始时间
            print(f"Successfully executed script: {file_path}")
        except oracledb.DatabaseError as e:
            print(f"Error executing script {file_path}: {e}")
        finally:
            cursor.close()


def insert_accident_data(dir_path):
    sql_scripts = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.sql')]
    # 使用 ThreadPoolExecutor 并行执行
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(execute_sql_script, sql_scripts)
    #execute_sql_script(sql_scripts[0])

if __name__ == "__main__":
    insert_accident_data("../sqlScripts/AccidentInserts")
