/*
* @Author: nfarrar
* @Date:   2014-10-31 13:50:45
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:59:27
*/

var http = require('http');
var server = http.createServer();

http.createServer(function(request, response) {
  var newFile = fs.createWriteStream("readme_copy.md");
  var fileBytes = request.headers['content-length'];
  var uploadedBytes = 0;

  request.on('readable', function() {
    var chunk = null;
    while(null !== (chunk = request.read())) {
      uploadedBytes += chunk.length;
      var progress = (uploadedBytes / fileBytes) * 100;
      response.write("progress: " + parseInt(progress, 10) + "%\n");
    }
  });
  request.pipe(newFile);

}).listen(8080);
