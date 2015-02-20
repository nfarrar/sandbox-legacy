/*
* @Author: nfarrar
* @Date:   2014-10-31 13:40:32
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:40:36
*/

var http = require('http');
var server = http.createServer();

server.on('request', function(request, response) {
  response.writeHead(200);
  response.write("Hello, this is dog");
  response.end();
});

server.on('request', function(request, response) {
  console.log("New request coming in...");
});

server.on('close', function() {
  console.log("Closing down the server...");
});


server.listen(8080);
