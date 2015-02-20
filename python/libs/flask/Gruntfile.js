// 'use strict';

/*global module:false*/
module.exports = function(grunt) {

  var pkgJSON = require('./package.json');

  var config = {
    pkg: pkgJSON,
    banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' +
            '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
            '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
            '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
            ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',
    src : 'bower_components',
    dist: 'app/static/'
    };

  // Project configuration.
  grunt.initConfig({

    // Load config
    config: config,

    // Metadata.
    pkg: config.pkg,
    banner: config.banner,

    // Task configuration.

    // grunt-bower-task
    bower: {
      install: {
        options: {
          targetDir: '<%= config.dist %>',
          install: true,
          cleanBowerDir: false,
          cleanTargetDir: false,
          layout: 'byType',
          copy: true,
          verbose: true,
          bowerOptions: {}
        }
      }
    },

    // grunt-contrib-concat
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      dist: {
        src: ['lib/<%= pkg.name %>.js'],
        dest: 'dist/<%= pkg.name %>.js'
      }
    },

    // grunt-contrib-uglify
    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      dist: {
        src: '<%= concat.dist.dest %>',
        dest: 'dist/<%= pkg.name %>.min.js'
      }
    },

    //grunt-contrib-jshint
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        unused: true,
        boss: true,
        eqnull: true,
        browser: true,
        ignores: ['Gruntfile.js'],
        globals: {}
      },
      gruntfile: {
        src: 'Gruntfile.js'
      },
      lib_test: {
        src: ['lib/**/*.js', 'test/**/*.js']
      }
    },

    // grunt-contrib-qunit
    qunit: {
      files: ['test/**/*.html']
    },

    // grunt-contrib-requirejs
    requirejs: {
      compile: {
        options: {
          findNestedDependencies: true,
          baseUrl: 'app/static/dist/js',
          mainConfigFile: 'app/static/local/js/require/options.js',
          out: 'app/static/local/js/require/optimized.js'
        }
      }
    },

    // grunt-contrib-watch
    watch: {
      gruntfile: {
        files: '<%= jshint.gruntfile.src %>',
        tasks: ['jshint:gruntfile']
      },
      lib_test: {
        files: '<%= jshint.lib_test.src %>',
        tasks: ['jshint:lib_test', 'qunit']
      }
    }

  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task.
  grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);

  /*
  grunt.registerTask('flask', 'Run flask development server.', function() {
    var spawn = require('child_process').spawn;
    var PIPE = {stdio: 'inherit'};
    grunt.log.writeln('Starting Flask development server.');
    var server = spawn('python', ['manage.py', 'runserver', '-t', '0.0.0.0'], PIPE);
    grunt.log.writeln('Started Flask development server.');
    process.on('exit', function() {
      grunt.log.writeln('killing myserver...');
      server.kill();
      grunt.log.writeln('killed myserver');
    });
  });
  */

  /*
  // start flask server - runs in background
  grunt.registerTask('flask', 'Run flask server.', function() {
    var spawn = require('child_process').spawn;
    grunt.log.writeln('Starting Flask development server.');
    // stdio: 'inherit' let us see flask output in grunt
    var PIPE = {stdio: 'inherit'};
    spawn('python', ['manage.py', 'runserver', '-t', '0.0.0.0'], PIPE);
  });
  */

  grunt.registerTask('server', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['build', 'open', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      'flask'
    ]);
  });

};
