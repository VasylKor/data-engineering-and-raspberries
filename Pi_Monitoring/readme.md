# Monitoring of hour PiS

A simple project born from the necessity to monitor my Pis.

You will find:
- `data_gathering` folder where a simple python script uses `psutils` to get hardware stats. Then a bash script which runs the script every 30 seconds and a service script to be put under `/etc/systemd/system/`. Then start the service and enable it to have it start at every reboot.
- `data_displaying` folder yet to be filled.