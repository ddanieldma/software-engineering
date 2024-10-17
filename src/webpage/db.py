import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

user=os.getenv("MYSQL_USER")
password=os.getenv("MYSQL_PASSWORD")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="coffe_map"
    )
