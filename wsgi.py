from app import create_app
import logging
from logging.handlers import RotatingFileHandler

application = create_app()

if __name__ == "__main__":
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    application.run(debug=True)