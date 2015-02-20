/*
* @Author: nfarrar
* @Date:   2014-10-31 13:59:18
* @Last Modified by:   nfarrar
* @Last Modified time: 2014-10-31 13:59:25
*/

var fs = require('fs');

var file = fs.createReadStream('fruits.txt');
02.js
file.on('readable', function(){
  var chunk;
  while(null !== (chunk = file.read())){
    console.log(chunk.toString());
  }
});
