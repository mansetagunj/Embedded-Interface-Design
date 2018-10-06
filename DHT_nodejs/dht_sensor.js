//@author - Gunj Manseta
//@node version - v8.12.0
//@reference - https://github.com/momenso/node-dht-sensor

//importing the  library
var sensor = require('./node_modules/node-dht-sensor');

console.log('Gunj Manseta Nodejs DHT22 interface EID HW4');

//reading from the sensor with DHT22 at pin 4
sensor.read(22, 4, function(err, temperature, humidity) {
    if (!err) {
	var tempdata = [];
	var humdata = [];
	var tempsum = 0;
	var humsum = 0
	for(i = 0; i < 10; i++){
	    tempdata[i] = ((temperature*1.8)+32).toFixed(1);
	    humdata[i] = humidity.toFixed(1);
	    tempsum = (tempsum + +tempdata[i]);
	    humsum = (humsum + +humdata[i]);
     	    console.log( i+1 + ' - Temp: ' + tempdata[i] + ' degF, ' + humdata[i] + '% Hum');
	}
	console.log('Lowest Temp ' + Math.min(...tempdata) + ' degF');
	console.log('Lowest Hum ' + Math.min(...humdata) + '%');
	console.log('Highest Temp ' + Math.max(...tempdata) + ' degF');
	console.log('Highest Hum ' + Math.max(...humdata) + '%');
	console.log('Average Temp ' + (tempsum/tempdata.length).toFixed(1) + ' degF');
	console.log('Average Hum ' + (humsum/humdata.length).toFixed(1) + '%');
    }
});
