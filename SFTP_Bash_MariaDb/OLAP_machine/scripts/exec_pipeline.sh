config=$1

. $config


if [ -d "$data_folder" ] 
then 
	if [ -d "$data_folder/$remote_filename" ] 
		then
			rm $data_folder/$remote_filename
			$scripts_folder/import.sh $path_to_main_folder/config/config.txt
			echo "Directory existed, data removed and imported"
		else
			$scripts_folder/import.sh $path_to_main_folder/config/config.txt
			echo "Directory existed, data imported"
		fi
else
	mkdir $data_folder 
	$scripts_folder/import.sh $path_to_main_folder/config/config.txt
	echo "Created directory and imported files"

fi
echo "Executing SQL pipeline"
python $scripts_folder/load_prices.py
echo "Done"