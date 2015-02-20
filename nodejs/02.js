/*
* @Author: nfarrar
* @Date:   2014-10-31 12:47:49
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 12:49:36
*/

var fs = require('fs');

var callback = function(err, contents) {
    console.log(contents)
}

fs.readFile('/etc/hosts', callback)
