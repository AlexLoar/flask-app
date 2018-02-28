from flask import Flask

from config import DefaultConfig

app = Flask(__name__)

app.config.from_object(DefaultConfig)

from users.views import users_page
app.register_blueprint(users_page)

from users.api import users_api
app.register_blueprint(users_api)

from persons.views import persons_page
app.register_blueprint(persons_page)
