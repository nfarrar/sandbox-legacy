/*
* @Author: nfarrar
* @Date:   2014-10-31 13:28:58
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:29:12
*/

var events = require('events');
var EventEmitter = events.EventEmitter;

var chat = new EventEmitter();
chat.on('message', function(message) {
  console.log(message);
});
