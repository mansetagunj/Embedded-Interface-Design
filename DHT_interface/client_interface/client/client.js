
$(document).ready(function(){
	//var socket = new WebSocket("ws://127.0.0.1:8888/ws");
	var socket = new WebSocket("ws://10.0.0.137:8888/ws");
    	
	socket.onerror = function(error){
		alert("Error Connecting to Server")
	}	
    
	socket.onclose = function(evt) {
		clearInterval(1000)
      		alert("Refresh the Webpage!");
    	}

	socket.onopen = function(evt) { 
		alert("websocket handshake performed!");
		setInterval(pingConnection, 1000);
		//var text = '{ "request" : [' +
		//'{ "entity":"load" , "type":"none" }'+
		//']}';
		//alert(text);
		//socket.send(text);
	}

	var messageParserAction = function(msg){
		//alert("Parsing");
		var parsedObj = JSON.parse(msg);
		var targetObj = "";
		if (parsedObj.response[0].entity == "temperature"){
			targetObj += "temp_";
		}
		else if (parsedObj.response[0].entity == "humidity"){
			targetObj += "hum_";
		}
		else{
			alert("Invalid Entity");
			return;
		}

		if(parsedObj.response[0].type == "latest"){
			targetObj += "p";
		}
		else if(parsedObj.response[0].type == "average"){
			targetObj += "a";
		}
		else if(parsedObj.response[0].type == "highest"){
			targetObj += "h";
		}
		else if(parsedObj.response[0].type == "lowest"){
			targetObj += "l";
		}
		else{
			alert("Invalid Entity type");
			return;
		}
		//alert("Target:" + targetObj);
		$("#" + targetObj).val(parsedObj.response[0].value);
		$("#timestamp").val(parsedObj.response[0].timestamp);
		
	}

	socket.onmessage = function(msgevt){
		//alert(msgevt.data);
		messageParserAction(msgevt.data);
	}

	var sendmessage = function(data){
		socket.send(data);
	}

	function pingConnection(){
		var text = '{ "ping" : "client"}';
		sendmessage(text);
	}

	$("#P_temp").click(function(){
	        var text = '{ "request" : [' +
			'{ "entity":"temperature" , "type":"latest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#A_temp").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"temperature" , "type":"average" }'+
			']}';
		sendmessage(text);
	});
	
	$("#H_temp").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"temperature" , "type":"highest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#L_temp").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"temperature" , "type":"lowest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#P_hum").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"humidity" , "type":"latest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#A_hum").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"humidity" , "type":"average" }'+
			']}';
		sendmessage(text);
	});
	
	$("#H_hum").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"humidity" , "type":"highest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#L_hum").click(function(evt){
		var text = '{ "request" : [' +
			'{ "entity":"humidity" , "type":"lowest" }'+
			']}';
		sendmessage(text);
	});
	
	$("#clear").click(function(evt) {
		
		});	
	
	function showimage(){
		document.getElementById('Image').style.visibility="visible";
	}

});