#!flask/bin/python

from website import website
from meraki.update import update

website.run(debug=True)
