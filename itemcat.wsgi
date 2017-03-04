import sys

sys.path.insert(0, '/var/www/html/itemcatalog/')
from main import app as application
application.secret_key = 'super_secret_key'
