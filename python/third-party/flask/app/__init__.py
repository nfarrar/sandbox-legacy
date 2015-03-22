from flask import Flask


#: Flask Application instance initialization
app = Flask(__name__)
app.config.from_object('app.config')


# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
# Test.jinja_env.globals['static'] = (
#     lambda filename: url_for('static', filename = filename)
# )


#: Intiliaze Application Level Views
from . import views
