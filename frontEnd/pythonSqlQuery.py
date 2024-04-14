import getpass
import time

import oracledb


# 数据库连接信息
cs = oracledb.makedsn('oracle.cise.ufl.edu', '1521', service_name='orcl')
un = 'h.zeng'
pw = 'POUvFYy9yY3KpPElxL4OGn9c'


def format_sql_commands(sql_commands):
    """
    This function takes in a list of SQL command strings, formats them according to the specified rules,
    and returns a list of strings representing the 1 line version of those commands.
    """
    formatted_commands = []
    current_command = ""

    for command in sql_commands:
        # Splitting the command into lines
        lines = command.split('\n')

        for line in lines:
            # Step 1: Remove -- and everything after it
            line = line.split('--')[0]
            # Step 2: Add a space to the end of the line
            line += " "
            # Step 4: Append the line to the current command
            current_command += line
            # Step 3: If the line ends with ;, add it to the list and reset current_command
            if line.strip().endswith(';'):
                formatted_commands.append(current_command.strip())
                current_command = ""

    # Ensure the last command is added if it doesn't end with a ;
    if current_command:
        formatted_commands.append(current_command.strip())

    return formatted_commands




def execute_sql_script(file_path):
    results=[]
    # 连接到数据库
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        # 创建一个新的游标
        cursor = connection.cursor()
        # 打开 SQL 文件并读取 SQL 命令
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.readlines()

        line_counter = 0  #
        start_time = time.time()
        sql_script = format_sql_commands(sql_script)
        try:
            for line in sql_script:
                line = line.strip().strip(';')
                if(len(line)<2 or line[0:2]=="--"):
                    continue
                # 执行 SQL 脚本
                if line:
                    result = []
                    for a in cursor.execute(line):
                        result.append(a)
                        line_counter += 1
                        if line_counter % 100000 == 0:
                            elapsed_time = time.time() - start_time
                            print(f"Executed 100000 lines in {elapsed_time:.2f} seconds")
                            start_time = time.time()  # 重置开始时间
                            results.append(result) #this should be deleted later
                            return results
            print(f"Successfully executed script: {file_path}")
            results.append(result)
        except oracledb.DatabaseError as e:
            print(f"Error executing script {file_path}: {e}")
        finally:
            cursor.close()
        return results

if __name__ == '__main__':
    print(execute_sql_script("../sqlScripts/selectAccidentData.sql"))
