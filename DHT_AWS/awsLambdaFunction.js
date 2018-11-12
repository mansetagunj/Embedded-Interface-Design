console.log('Loading function');

var QUEUE_URL = 'qURL.fifo';
var AWS = require('aws-sdk');
var sqs = new AWS.SQS({region : 'us-east-2'});
var count = 0;
var minT = 0;
var maxT = 0;
var avgT = 0;
var minH = 0;
var maxH = 0;
var avgH = 0;

exports.handler = (event, context) => {
  
  if(count == 0){
    minH = event.humidity;
    maxH = event.humidity;
    avgH = event.humidity;
    minT = event.temperature;
    maxT = event.temperature;
    avgT = event.temperature;
  }
  else{
    minH = Math.min(minH, event.humidity);
    maxH = Math.max(maxH, event.humidity);
    avgH = (((avgH*count) + parseFloat(event.humidity)) / (count+1)).toFixed(2);
    minT = Math.min(minT, event.temperature);
    maxT = Math.max(maxT, event.temperature);
    avgT = (((avgT*count) + parseFloat(event.temperature)) / (count+1)).toFixed(2);
  }
  
  event.minH = minH;
  event.maxH = maxH;
  event.avgH = avgH
  event.minT = minT;
  event.maxT = maxT;
  event.avgT = avgT;
  
  count++;
  
  var data = JSON.stringify(event, null, 2);
  console.log('Received event:', data);
  var success = sendMessageQ(data, context);
  if(!success){
    console.log('Send Message Error');
  }
  return event.key1; 
};

function sendMessageQ(data,context){
    
    var params = {
    MessageBody: data,
    QueueUrl: QUEUE_URL,
    DelaySeconds: 0,
    MessageGroupId: '1'
    };
    
    sqs.sendMessage(params, function(err,data){
      if(err) {
        console.log('error:',"Failed to write to queue -" + err);
        context.done('error', "ERROR writing to SQS");
        return false;
      }else{
        console.log('data:',data.MessageId);
        context.done(null,'');
        return true;
      }
    });
}

