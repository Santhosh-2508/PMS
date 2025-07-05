import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MasterConfig:
    def __init__(self, host='localhost', database='hotel_management system', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):      
        try:
            self.connection = mysql.connector.connect(
                host=self.host, 
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                logging.info("Connected to the database")               