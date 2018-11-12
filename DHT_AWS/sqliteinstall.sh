#!/bin/bash

sudo apt-get install sqlite &&
sqlite3 .exit

read -p "Do you want to install DB viewer GUI tool?(yes/no) >" ans
if [ "$ans" == "y" ] || [ "$ans" == "Y" ] || [ "$ans" == "yes" ] || [ "$ans" == "Yes" ]; then
	echo 'Installing sqliteman'
	sudo apt-get install sqlitebrowser
else
	echo 'exit'
fi
