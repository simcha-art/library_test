from logs.logger_config import logger
import mysql.connector

class DB:
    def __init__(self):
        self.conn = self.get_connection()
        self.create_tables()


    def get_connection(self):
        logger.info("start connecting to docker container...")
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "simcha-2001"
        )
        logger.info("connected to docker container successfully")
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS library_db;")
        if cursor.warning_count == 0:
            logger.warning("created a new database - library_db")
        cursor.execute("USE library_db;")
        logger.info("connected to database library_db")
        cursor.close()
        return conn


    def create_tables(self):
        cursor = self.conn.cursor()
        query_books = """
        CREATE TABLE IF NOT EXISTS books (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL, 
        genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other"),
        is_available BOOLEAN DEFAULT TRUE,
        borrowed_by_member_id INT 
        );
        """
        cursor.execute(query_books)
        if cursor.warning_count == 0:
            logger.warning("created new table books")

        query_members = """
        CREATE TABLE IF NOT EXISTS members (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE, 
        is_active BOOLEAN DEFAULT TRUE,
        total_borrows INT DEFAULT 0
        );
        """
        cursor.execute(query_members)
        if cursor.warning_count == 0:
            logger.warning("created new table members")
    

db = DB()