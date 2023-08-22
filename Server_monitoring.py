import psutil
import platform
from datetime import datetime, timedelta
import mysql.connector
import time
import json

update_interval_hf_minutes = 10  # Update every 2 minutes
update_interval_lf_days = 17   # Update every 30 days

update_interval_hf_seconds = update_interval_hf_minutes #* 60
update_interval_lf_seconds = update_interval_lf_days #* 24 * 60 * 60

next_update_time_hf = datetime.now() + timedelta(seconds=update_interval_hf_seconds)
next_update_time_lf = datetime.now() + timedelta(seconds=update_interval_lf_seconds)

mydb = mysql.connector.connect(host='localhost', user='root', password='m253769a@mysql')

cur = mydb.cursor()

cur.execute("use CPU;")
cur.execute("DROP TABLE IF EXISTS SystemStatus_hf;")
cur.execute("DROP TABLE IF EXISTS SystemStatus_lf;")
cur.execute("CREATE TABLE SystemStatus_hf (Server_Name VARCHAR(50), IP_Address VARCHAR(15), MAC VARCHAR(17), RAM_Util DECIMAL(5,2), CPU_Util DECIMAL(5,2), Storage_Util DECIMAL(5,2), Last_Uptime DATETIME, Timestamp TIMESTAMP);")
cur.execute("CREATE TABLE SystemStatus_lf (Server_Name VARCHAR(50), IP_Address VARCHAR(15), MAC VARCHAR(17), OS_Version VARCHAR(50), System_RAM DECIMAL(5,2), number_of_cores INT, Storage_Capacity DECIMAL(10,2), Timestamp TIMESTAMP);")

# Read server information from the JSON file
with open('Data_ADD/servers.json') as f:
    servers = json.load(f)

while True:
    for server in servers:
        ip_address = server["ip_address"]
        mac_address = server["mac_address"]
        os_version = f"{platform.system()} {platform.release()} {platform.version()}"
        system_ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
        number_of_cores = psutil.cpu_count(logical=False)
        storage_capacity = psutil.disk_usage('/').total / (1024 ** 3)  # Convert to GB

        cur.execute("INSERT INTO SystemStatus_hf (Server_Name, IP_Address, MAC, RAM_Util, CPU_Util, Storage_Util, Last_Uptime, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (server["name"], ip_address, mac_address, 0, 0, 0, datetime.now(), datetime.now()))

        cur.execute("INSERT INTO SystemStatus_lf (Server_Name, IP_Address, MAC, OS_Version, System_RAM, number_of_cores, Storage_Capacity, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (server["name"], ip_address, mac_address, os_version, system_ram, number_of_cores, storage_capacity, datetime.now()))

        mydb.commit()

    for server in servers:
        cur_time = datetime.now()
        while (datetime.now() - cur_time).total_seconds() < update_interval_hf_seconds:
            # Collect system data
            ip_address = server["ip_address"]
            mac_address = server["mac_address"]

            memory = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()
            storage = psutil.disk_usage('/').percent

            last_uptime_timedelta = timedelta(seconds=int(time.time() - psutil.boot_time()))
            last_uptime_datetime = datetime.now() - last_uptime_timedelta
            last_uptime_formatted = last_uptime_datetime.strftime('%Y-%m-%d %H:%M:%S')

            system_ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
            number_of_cores = psutil.cpu_count(logical=False)
            storage_capacity = psutil.disk_usage('/').total / (1024 ** 3)  # Convert to GB
            os_version = f"{platform.system()} {platform.release()} {platform.version()}"

            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            if datetime.now() >= next_update_time_hf:
                cur.execute("INSERT INTO SystemStatus_hf (Server_Name, IP_Address, MAC, RAM_Util, CPU_Util, Storage_Util, Last_Uptime, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (server["name"], ip_address, mac_address, memory, cpu_percent, storage, last_uptime_formatted, formatted_time))

                mydb.commit()

                next_update_time_hf += timedelta(seconds=update_interval_hf_seconds)
                print("Updating SystemStatus_hf at:", datetime.now())
                print("----------------------------------------")

            if datetime.now() >= next_update_time_lf:
                cur.execute("INSERT INTO SystemStatus_lf (Server_Name, IP_Address, MAC, OS_Version, System_RAM, number_of_cores, Storage_Capacity, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (server["name"], ip_address, mac_address, os_version, system_ram, number_of_cores, storage_capacity, formatted_time))

                mydb.commit()

                next_update_time_lf += timedelta(seconds=update_interval_lf_seconds)
                print("Updating SystemStatus_lf at:", datetime.now())
                print("----------------------------------------")

            time.sleep(1)  # Wait for 1 second before the next iteration
        cur_time = datetime.now()

cur.close()
mydb.close()