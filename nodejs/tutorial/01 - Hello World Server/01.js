/*
* @Author: nfarrar
* @Date:   2014-10-31 12:51:15
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:04:38
*/

var http = require('http');

http.createServer(function(request, response) {
  response.writeHead(200);          // status code in header
  response.write("Hello world!");   // response body
  response.end();                   // close the connection
}).listen(8080);                    // port to listen on

console.log('Listening on port 8080')


// node helloworld-server.js
// curl localhost:8080
// Hello world!%
