import logging
from logging.handlers import RotatingFileHandler
from datetime import date

from src import app

handler = RotatingFileHandler('log_{}.log'.format(date.today().strftime('%Y-%m-%d')), maxBytes=10000, backupCount=1)
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

app.run(debug=True, host='0.0.0.0')
