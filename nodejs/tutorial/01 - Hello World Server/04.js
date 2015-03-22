/*
* @Author: nfarrar
* @Date:   2014-10-31 13:38:37
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:40:38
*/

var http = require('http');

var server = http.createServer();

server.on('request', function(request, response) {
  response.writeHead(200);
  response.write("Hello, this is dog");
  response.end();
});
server.listen(8080);
