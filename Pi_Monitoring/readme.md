
# Monitor our Pis


A simple project born from the necessity to monitor my Pis. Works with **mariadb**.

You will find:

- `data_gathering` folder where a simple Python 3.9 script uses `psutils` to get hardware stats. Then a bash script which runs the script every 30 seconds and a service script to be put under `/etc/systemd/system/`. Then start the service and enable it to have it start at every reboot.
  Dependencies:

  - psutil (`pip install psutil`)

  - mariadb connector (`pip install mariadb`) 
    I had also to:

    ```shell
    sudo apt install mariadb-server
    sudo apt install mariadb-client
    sudo apt install libmariadb-dev
    sudo apt install libmariadb-dev-compat
    ```

- `data_displaying` folder where Dash is used to run a server on which stats from `data_gathering` are displayed. Works but must be enhanced for perfomance.
