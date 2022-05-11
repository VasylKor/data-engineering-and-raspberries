config=$1

. $config


if [ -d "$path_to_main_folder/logs/logs.txt" ]
	then
		echo "Logs Exist"
	else
		touch $path_to_main_folder/logs/logs.txt
fi

echo "----------New Execution----------" >> $path_to_main_folder/logs/logs.txt

if [ -d "$data_folder" ] 
then 
	$scripts_folder/import.sh $path_to_main_folder/config/config.txt
	echo `date` "Directory existed, data imported" >> $path_to_main_folder/logs/logs.txt
else
	mkdir $data_folder 
	$scripts_folder/import.sh $path_to_main_folder/config/config.txt
	echo `date` "Created directory and imported files" >> $path_to_main_folder/logs/logs.txt

fi
echo `date` "Executing SQL pipeline" >> $path_to_main_folder/logs/logs.txt
python $scripts_folder/load_prices.py 
echo `date` "Done" >> $path_to_main_folder/logs/logs.txt