from flask_script import Server
from . import manager


#: Add development defaults to the runserver command
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)
