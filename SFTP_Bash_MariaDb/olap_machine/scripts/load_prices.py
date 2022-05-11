import configparser
import numpy as np
import pandas as pd
import mariadb
import os
import sys

# Setting folder as working directory
os.chdir(os.path.dirname(sys.argv[0]))

# Reading configuration
config = configparser.ConfigParser()
config.read("../config/py_config.txt")
db_param = config["mariadb"]
sys_param= config["system"] 
data_path = sys_param["data_folder"]+sys_param["data_filename"]
processed_data_path = sys_param["data_folder"]+sys_param["processed_data_filename"]

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

data = pd.read_csv(data_path)
data['Datetime'] = pd.to_datetime(data['Datetime'])
# getting Id as int taken from datetime -- makes assumptions
# on how pandas stores datetime
data['Id'] = data['Datetime'].astype(int) / 10**9

# Setting datetime in format accepted by Mariadb
data['Datetime'] = data['Datetime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
data = data.fillna(data.mean())

# Bringing Id as first column
cols = list(data.columns)
cols = [cols[-1]] + cols[:-1]
data = data[cols]

data.to_csv(processed_data_path, index=False, header=False)

cur = conn.cursor()
cur.execute(f"TRUNCATE TABLE {dest_table}")
cur.execute(
	f"LOAD DATA INFILE '{processed_data_path}' INTO TABLE {dest_table} FIELDS TERMINATED BY ',';")
cur.execute("CALL finance.pr_UpdateACP")
conn.commit()
conn.close()