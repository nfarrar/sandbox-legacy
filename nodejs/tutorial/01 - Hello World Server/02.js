/*
* @Author: nfarrar
* @Date:   2014-10-31 12:57:09
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:05:14
*/

var http = require('http');

http.createServer(function(request, response) {
  response.writeHead(200);          // status code in header
  response.write("Hello world!");   // response body

  // Set a callback that simulates a long running process.
  // This
  setTimeout(function() {
    response.write("Goodbye world.");
    response.end();
  }, 5000);                         // pause for 5000ms (5 seconds)

}).listen(8080);

console.log('Listening on port 8080')

// node helloworld-server.js
// curl localhost:8080
// 2 second pause ...
// Hello world!Goodbye world.%
