Repo for Fall 2018 Embedded Interface Design class
# Name: Gunj Manseta & Shreya Chakraborty
For Project2
Referernces:
1.  https://www.tutorialspoint.com/python/python_date_time.htm 
2.  https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/ 
3.  https://stackoverflow.com/questions/11812000/login-dialog-pyqt 
4.  https://pythonspot.com/pyqt5/ 
5.  Adafruit packages for the DHT-22  
6.  https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_button_group_justified
7.  https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_pills_dynamic&stacked=h
8.  https://www.stackoverflow.com
9.  https://os.mbed.com/cookbook/Websockets-Server
10. https://www.tornadoweb.org/en/stable/websocket.html

# INSTALLATION INSTRUCTIONS:
Run this project on the server rpi using the following command on terminal : ./DHTApplication.py
Run this project on the client by clicking index.html

# PROJECT WORK :
The project is a joint effort by Gunj Manseta and Shreya Chakraborty. Any similarities with anyone else's work other than the ones 
specified in the references is purely coincidental. The Project is a continuation to project1.In project 1 we interfaced a temp/humidity
sensor DHT-22 with RPI and design a UI to display the current temperature, humidity, time of requesting, the status of the sensor 
and so on.In this project, there are two rpi one client and other server. The server rpi is interfaced with the sensor and gather data periodically and stores it in a data base. The latest values, avg values, min and max values are computed from the values in the database and the serverthen sends these values over to the client. The javascript at the client side sorts out the data and displays the hmtl page with various buttons. The corresponding values along with the timestamp are displayed on the client side on button press. Prior to that the client displays a login screen. The username is "project2" and the password is "123456". On entering correct credentials the main "weather report" html page is displayed.
 
# NECESSARY INSTALLATIONS FOR THE PROJECT 2
1. tornado using the command: $ sudo pip install tornado
2. SQLite for database : $sudo apt-get install mysql-server python-mysqldb
3. matplotlib for graph: $sudo apt-get install python3-matplotlib
4. node.js :$ curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash 
           :$ sudo apt install -y nodejs

# PROJECT ADDITIONS :
The following extra credit options have been attempted
1.  A login screen to secure the application on the client side.
2.  Multi-threading 
3.  A nice interface with background, popup messages, multiple tabs namely - Home, graph,Readme and links. 
4.  IP address is configurable.
