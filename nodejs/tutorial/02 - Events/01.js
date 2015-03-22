/*
* @Author: nfarrar
* @Date:   2014-10-31 13:24:24
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:25:41
*/

var EventEmitter = require('events').EventEmitter;

var logger = new EventEmitter();

logger.on('error', function(message) {
    console.log('ERR: ' + message)
});

logger.emit('error', 'error 1');
logger.emit('error', 'error 2');
