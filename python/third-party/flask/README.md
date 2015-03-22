## flask_skeleton

## Base Dependencies
Install basic development dependencies:

    # core build
    sudo apt-get install -y autoconf automake bison build-essential gawk gcc linux-headers-$(uname -r) make
    sudo apt-get install -y ca-certificates curl wget
    sudo apt-get install -y foreman

    # version control
    sudo apt-get install -y git mercurial subversion

    # python
    sudo apt-get -y install bpython ipython python python-dev python-pip python-software-properties python-setuptools

    # ruby
    sudo apt-get install -y ruby ruby-dev rubygems

    # sqlite
    sudo apt-get install -y sqlite3

## Git, hub & gitignore.io
Install hub wrapper for git:

    BIN_DIR='$HOME/.bin'
    BASH_FUNCTIONS='$HOME/.bash/functions'

    $ALIAS_FILE
    mkdir -p ~/.bin
    curl http://hub.github.com/standalone -sLo ~/$BIN_DIR/hub
    chmod +x ~/$BIN_DIR/hub

    echo "function gi() { curl http://gitignore.io/api/\$@ ;}" >> ~/$BASH_FUNCTIONS && source ~/.bash_profile

## Virtualenv & Virtualenvwrapper
Install virtualenv and virtualenv-wrapper:

    sudo pip install virtualenv virtualenv-wrapper

    mkdir -p ~/.virtualenv
    echo "export WORKON_HOME="$HOME/.virtualenv"
    source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

    source ~/.bashrc

## Node & NPM
Install nodejs and npm:

    sudo add-apt-repository -y ppa:chris-lea/node.js
    sudo apt-get install -y nodejs
    sudo ln -s /usr/bin/nodejs /usr/bin/node
    curl https://npmjs.org/install.sh | sudo sh

## Heroku Toolbelt
Install heroku toolbelt:

    wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sudo sh

## Grunt & Bower
Install grunt & bower:

    sudo npm install -g grunt grunt-cli grunt-init bower
    git clone https://github.com/gruntjs/grunt-init-gruntfile.git ~/.grunt-init/gruntfile

## Project Creation
These instructions describe how to create a new project using the described workflow from scratch, to create a new
project skip below to 'Project Cloning'.

Create the project directory and github repository:

    PROJ='flask_skeleton'
    mkdir $PROJ && cd $PROJ
    git init
    git create $PROJ

Create the project directory structure:

    mkdir -p {app/{static,templates},docs,tmp}

Create & activate the virtual environment.  Install flask modules:

    mkvirtualenv flask_skeleton
    pip install flask Frozen-Flask Flask-SQLAlchemy Flask-Login Flask-Principal flask-script flask-wtf flask-debugtoolbar
    pip freeze > requirements.txt

Initialize the npm package configuration (package.json):

    npm init

Configuration settings:

    # name: (FlaskSkeleton)
    # version: (0.0.0)
    # description: FlaskSkeleton
    # entry point: (Gruntfile.js)
    # test command: grunt test
    # git repository: (git://github.com/nfarrar/sandbox.git)
    # keywords: flask node npm grunt bower
    # author: Nathan Farrar
    # license: (BSD-2-Clause) MIT

Install npm packages & save configuration:

    npm install grunt grunt-shell bower grunt-bower-task grunt-contrib-concat grunt-contrib-jshint grunt-contrib-qunit
    grunt-contrib-requirejs grunt-contrib-uglify grunt-contrib-watch --save-dev

Initialize the grunt configuration (Gruntfile.js):

    grunt-init gruntfile

Configuration settings:

    # Please answer the following:
    # [?] Is the DOM involved in ANY way? (Y/n) Y
    # [?] Will files be concatenated or minified? (Y/n) Y
    # [?] Will you have a package.json file? (Y/n) Y
    # [?] Do you need to make any changes to the above before continuing? (y/N) N

Grab the [finalized configurationn](https://raw.github.com/oxsyn/FlaskSkeleton/master/Gruntfile.js) and dump it into
Gruntfile.js.

Create the .editorconfig file in the root directory:

    cat > .editorconfig <<EOL
    # This file is for unifying the coding style for different editors and IDEs.
    # More information at http://EditorConfig.org

    # No .editorconfig files above the root directory
    root = true

    [*]
    indent_style = space
    end_of_line = lf
    charset = utf-8
    trim_trailing_whitespace = true
    insert_final_newline = true

    # Use 2 spaces for indentation in HTML, JavaScript, JSON and XML

    [*.{htm,html,js,json,xml}]
    indent_size = 2

    # Use 4 spaces for indentation in Markdown and Python files

    [*.{md,python}]
    indent_size = 4
    EOL

Create the .gitignore file:

    gi linux,osx,windows,python,ruby > .gitignore
    cat >> .gitignore <<EOL

    ### Project ###
    bower_components/*
    node_modules/*
    EOL

Create the .bowerrc file:

    cat >> .bowerrc <<EOL
    {
        "directory": "lib/bower_components",
        "json": "bower.json"
    }
    EOL

Generate the bower.json configuration file:

    bower init

Configuration Settings:

    [?] name: FlaskSkeleton
    [?] version: 0.0.0
    [?] description: FlaskSkeleton
    [?] main file:
    [?] keywords: flask, bower, grunt
    [?] authors: Nathan Farrar
    [?] license: MIT
    [?] homepage: https://github.com/sandbox/flask_skeleton
    [?] set currently installed components as dependencies? Yes
    [?] add commonly ignored files to ignore list? Yes
    [?] would you like to mark this package as private which prevents it from being accidentally published to the regist[?] would you like to mark this package as private which prevents it from being accidentally published to the registry? Yes

Install our bower components & save the configuration:

    bower install bootstrap font-awesome html5shiv jquery modernizr requirejs respond --save

To bootstrap the bower installation process with grunt, add the exportsOverride section to bower.json from the
[finalized configuration](https://raw.github.com/oxsyn/FlaskSkeleton/master/bower.json).

Install the flask favicon:

    curl -O http://flask.pocoo.org/static/favicon.ico app/static/favicon.ico

## References


### Node & NPM

+ [npm 1.0: Global vs Local installation](http://blog.nodejs.org/2011/03/23/npm-1-0-global-vs-local-installation/)
+ [package.jsonAn interactive guide](http://package.json.nodejitsu.com/)
+ [npm cheatsheet](http://blog.nodejitsu.com/npm-cheatsheet)

### Heroku

+ [Process Types and the Procfile](https://devcenter.heroku.com/articles/procfile)
+ [heroku toolbelt: everything you need to get started using heroku](https://toolbelt.heroku.com/debian)
+ [The Celadon Cedar Stack](https://devcenter.heroku.com/articles/cedar)
+ [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
+ [Dynos and the Dyno Manager](https://devcenter.heroku.com/articles/dynos)

### Misc

+ [Meet Bower: A Package Manager For The Web](http://net.tutsplus.com/tutorials/tools-and-tips/meet-bower-a-package-manager-for-the-web/)
+ http://samrat.me/blog/2012/05/flask-nginx-gunicornon-a-vagrant-box/
+ http://blog.codeship.io/2013/11/07/building-vagrant-machines-with-packer.html

### Grunt

+ [Compiling CoffeeScript with grunt](http://takazudo.github.io/blog/entry/2012-04-14-grunt-coffee.html)
+ [Make Grunt watch for LESSCSS changes](http://jonathanmh.com/make-grunt-watch-for-lesscss-changes/)
+ https://www.youtube.com/watch?v=q3Sqljpr-Vc
+ https://www.youtube.com/watch?v=s5eBIie03ls
+ https://www.youtube.com/watch?v=H9WXnwy2C00
+ http://net.tutsplus.com/tutorials/javascript-ajax/meeting-grunt-the-build-tool-for-javascript/
+ http://merrickchristensen.com/articles/gruntjs-workflow.html
+ http://takazudo.github.io/blog/entry/2012-04-14-grunt-coffee.html
+ http://jonathanmh.com/make-grunt-watch-for-lesscss-changes/
