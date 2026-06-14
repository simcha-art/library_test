from database.db_connection import db
from logs.logger_config import logger

class BookDB:
    def __init__(self):
        pass

    def create_book(self, data: dict):
        logger.info("start creating a new book")
        with db.conn.cursor(dictionary=True) as cursor:
            title = data.get("title")
            author = data.get("author")
            genre = data.get("genre")
            VALID_GENRE = ["Fiction", "Non-Fiction",  "Science", "History", "Other"]
            if genre not in VALID_GENRE:
                logger.error(f"could not create the book, genre must be from {VALID_GENRE}")
                return None
            query = """
            INSERT INTO books
            (title, author, genre)
            VALUES
            (%s, %s, %s)
            """
            params = [title, author, genre]
            cursor.execute(query, params)
            db.conn.commit()
            new_id = cursor.lastrowid
            if not new_id:
                logger.error("could not create the book")
                return None
            logger.info(f"book {new_id} {title} created successfully")
            return new_id
    

    def get_all_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting list of all books...")
            cursor.execute("SELECT * FROM books;")
            books = cursor.fetchall()
            if not books:
                logger.warning("There are no books in library")
                return {"msg": "There are no books in library"}
            logger.info("books list returned")
            return books
        
    def get_book_by_id(self, book_id: int):
        logger.info(f"start getting book by id: {book_id}")
        with db.conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT * FROM books
            WHERE id = %s
            """
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()
            if not book:
                logger.error(f"book {book_id} not found")
                return {"msg": f"book {book_id} not found"}
            logger.info(f"book {book_id} returned successfully")
            return book
        
    def update_book(self, id: int, data: dict):
        set_clause = ", ".join(f"{field} = %s" for field in data.keys())
        query = f"""
        UPDATE books
        SET
        {set_clause}
        WHERE id = %s
        """

        values = [val for val in data.values()]
        params = values + [id]

        logger.info(f"start updating book {id}")
        with db.conn.cursor() as cursor:
            cursor.execute(query, params)
            success = cursor.rowcount > 0
            db.conn.commit()


        if success:
            logger.info("update complete")
        else:
            logger.error("update failed")

        return success
    
    def set_available(self, id: int, val: bool, member_id: int | None = None):
        data = {
                "is_available": val,
                "borrowed_by_member_id": member_id
                    }
        self.update_book(id, data)
        return True

    def count_all_books(self):
        logger.info("start count all books...")
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM books")
            total = cursor.fetchall()[0]["total"]
            logger.info("complete count all books")
            if total == 0:
                logger.warning(f"There are no books in library")
            return total
            

    def count_available_books(self):
        logger.info("start count available books...")
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS available_books FROM books WHERE is_available = TRUE")
            avail = cursor.fetchall()[0]["available_books"]
            logger.info("complete count available books")
            if avail < 5:
                logger.warning("Too few books available")
            return avail
        
    
    def count_borrowed_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS borrowed FROM books WHERE is_available = FALSE")
            return cursor.fetchall()[0]["borrowed"]
        
    def count_by_genre(self, genre):
        query = """
        SELECT COUNT(*) AS total FROM books WHERE genre = %s
        """
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (genre,))
            return cursor.fetchall()[0]["total"]
        

    def count_active_borrows_by_member(self, member_id: int):
        query = """
        SELECT COUNT(*) AS total FROM books 
        WHERE borrowed_by_member_id = %s
        """
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (member_id,))
            return cursor.fetchall()[0]["total"]







book_manager = BookDB()
