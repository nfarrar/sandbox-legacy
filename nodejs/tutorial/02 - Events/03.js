/*
* @Author: nfarrar
* @Date:   2014-10-31 13:30:51
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:33:39
*/

var events = require('events');
var EventEmitter = events.EventEmitter;

var chat = new EventEmitter();
var users = [], chatlog = [];

chat.on('message', function(message) {
  chatlog.push(message);
});

chat.on('join', function(nickname) {
  users.push(nickname);
});

// Emit events here
chat.emit('join', "Someone");
chat.emit('message', "Some Message.");
