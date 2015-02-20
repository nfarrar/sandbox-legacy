#!/usr/bin/env python

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine
from flask_script import Manager


#: Flask Application Instance
app = Flask(__name__)

#: Flask Configuration
app.config['DEBUG'] = True
app.config['TESTING'] = True


#: Flask-MongoEngine Extension Instance
db = MongoEngine(app)

#: Flask-Script Manager extension instance
manager = Manager(app)


#: Flask DebugToolBar extension instance
toolbar = DebugToolbarExtension(app)



if __name__ == '__main__':
    manager.run()
