

import mysql.connector
import time
import os
from dotenv import load_dotenv

load_dotenv()

def env(name):
    return os.getenv(name)






mydb = mysql.connector.connect(
    host=env("HOST"),
    user=env("DB_UNAME"),
    password=env("DB_PASS"),
    database=env("DB_NAME"),
)


