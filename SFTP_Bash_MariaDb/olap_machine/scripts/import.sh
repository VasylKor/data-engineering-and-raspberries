config=$1

. $config

cd $data_folder
sftp $remote_machine_user@$remote_machine_hostname << DELIM 
	get $remote_file_path/$remote_filename
	exit
DELIM