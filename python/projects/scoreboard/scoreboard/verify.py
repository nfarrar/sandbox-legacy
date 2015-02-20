#!/usr/bin/env python

import os

from flask import Flask, flash, render_template, request
from flask_script import Manager
from wtforms import Form, TextField
from wtforms.validators import Required

#: Flask instance intialization
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.password = "sekret"

#: Flask manager instance initialization
manager = Manager(app)


class KeyForm(Form):
    name = 'Key Verifier'
    key = TextField('Key', description='Key', validators=[Required()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = KeyForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.key.data == app.password:
            flash('Key Correct.', 'success')
        else:
            flash('Key Incorrect.', 'danger')
    return render_template('index.htm', form=form)


if __name__ == '__main__':
    manager.run()
