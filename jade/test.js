var jade   = require('jade'),
    merge  = require('merge'),
    config = require('./config'),
    locals = require('./locals');

var html = jade.renderFile('test.jade', merge(config, locals));
console.log(html)
