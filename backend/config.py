import logging
import time
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

# Environment variables
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("cpy-errors.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 

config = {
  'user': USER,
  'password': PASSWORD,
  'host': HOST,
  'database': DATABASE,
  'raise_on_warnings': True
}

def connect_to_mysql(config=config, attempts=3, delay=2):
    attempt = 1
    # Implement a reconnection routine
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if (attempts is attempt):
                # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None
