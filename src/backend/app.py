from flask import Flask
from endpoints.home import home_blueprint

app = Flask(__name__)
app.register_blueprint(home_blueprint)

