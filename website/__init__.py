from flask import Flask

website = Flask(__name__)
website.config.from_object('config')
from website import home
