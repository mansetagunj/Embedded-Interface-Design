# eid-fall2018
Repo for Fall 2018 Embedded Interface Design class
# Name: Gunj Manseta & Shreya Chakraborty
For Project4
Referernces:
1.  https://www.tutorialspoint.com/python/python_date_time.htm 
2.  https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/ 
3.  https://stackoverflow.com/questions/11812000/login-dialog-pyqt 
4.  Adafruit packages for the DHT-22  
5.  https://websockets.readthedocs.io/en/stable/intro.html
6. 	https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
7. 	https://www.geeksforgeeks.org/zip-in-python/
8. 	https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs-example-sending-receiving-msgs.html
9.  https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3
10. http://coapy.sourceforge.net/
11. https://www.apptic.me/blog/getting-started-with-websockets-in-tornado.php
12. https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
13. http://coap.technology/


# INSTALLATION INSTRUCTIONS:
Run this project on the server rpi using the following command on terminal : ./DHTApplication.py
Run this project on the client rpi using by the following command on terminal : ./application.py

# PROJECT WORK :
The project is a joint effort by Gunj Manseta and Shreya Chakraborty. Any similarities with anyone else's work other than the ones 
specified in the references is purely coincidental. The Project is a continuation to project1 and project 2.In project 1 we interfaced a temp/humidity sensor DHT-22 with RPI and design a UI to display the current temperature, humidity, time of requesting, the status of the sensor and so on.In project 2, there were two rpi one client and other server. The server rpi is interfaced with the sensor and gather data periodically and stores it in a data base. The latest values, avg values, min and max values are computed from the values in the database and the server then sends these values over to the client. The javascript at the client side sorts out the data and displays the hmtl page with various buttons. In this current Project 4 the server side rpi periodically measure the temperature and humidity every 5 secs displays it in the server side QT and sends  it over to amazon AWS IOT using 3 protocols - MQTT , websockets and CoAP. The execution time for the message exchange are calculated and displayed on a table on the client side along with a graphical comparison in addition to  the previous graphs of temp and humidity with 4 lines each. Based on our comparison we find that Websockets are the fastest.

 
# NECESSARY INSTALLATIONS FOR THE PROJECT 2
1. tornado using the command: $ sudo pip install tornado
2. SQLite for database : $sudo apt-get install mysql-server python-mysqldb
3. matplotlib for graph: $sudo apt-get install python3-matplotlib
4. node.js :$ curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash 
           :$ sudo apt install -y nodejs
5. install boto using the command : pip3 install boto3
6. install webscokets : pip install websocket-client

# PROJECT ADDITIONS :
The following extra credit options have been attempted
1.  A login screen to secure the application on the client side. The Username is 'shreya' and the password is 'eid'
2.  Multi-threading 

