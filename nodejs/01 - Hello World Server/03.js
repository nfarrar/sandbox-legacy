/*
* @Author: nfarrar
* @Date:   2014-10-31 13:16:41
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:21:36
*/

var http = require('http');
var fs = require('fs');

http.createServer(function(request, response) {
  response.writeHead(200, {
  'Content-Type': 'text/plain' });

  fs.readFile('03.js', function(error, contents) {
    response.write(contents)
  });

}).listen(8080);

console.log('Listening on port 8080')
