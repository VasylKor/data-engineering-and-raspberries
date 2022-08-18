import psutil
import mariadb
import configparser
import os
import sys


# Setting folder as working directory
os.chdir(os.path.dirname(sys.argv[0]))

# Reading configuration
config = configparser.ConfigParser()
config.read("../config/py_config.txt")
db_param = config["mariadb"]

dest_table = db_param["dest_table"]

try:
	conn = mariadb.connect(
	user=db_param["user"],
	password=db_param["pwd"],
	host=db_param["host"],
	port=int(db_param["port"]),
	database=db_param["schema"]

	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

# Get CPU stats

cpu_percent = psutil.cpu_percent(interval=2)


# Get RAM usage in bytes

ram_usage = psutil.virtual_memory().percent
ram_available = psutil.virtual_memory().available
ram_used = psutil.virtual_memory().used
ram_swap_percent = psutil.virtual_memory().available


# Get Disk usage in bytes

disk_percent = psutil.disk_usage('/').percent
disk_used = psutil.disk_usage('/').used
disk_free = psutil.disk_usage('/').free


# Get CPU temperature in °C, if not present then it's -99

cpu_temp = psutil.sensors_temperatures()
## looking for cpu_thermal in dictionary
for x in ['cpu-thermal', 'cpu_thermal']:
    if x in cpu_temp:
        cpu_temp = cpu_temp[x][0].current

if type(cpu_temp) is dict:
    cpu_temp = -99



# Get Network statistics in bytes

net_sent = psutil.net_io_counters(pernic=False, nowrap=True).bytes_sent
net_received = psutil.net_io_counters(pernic=False, nowrap=True).bytes_recv







