from database.db_connection import db
from logs.logger_config import logger

class MemberDB:

    def create_member(self, data: dict):
        name = data.get("name")
        email = data.get("email")
        query = """
        INSERT INTO members
        (name, email)
        VALUES
        (%s, %s)
        """
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (name, email))
            db.conn.commit()
            new_id = cursor.lastrowid
            logger.info(f"member {new_id} created successfully")
        return new_id
    

    def get_all_members(self):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()
        

    def get_member_by_id(self, member_id: int):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            return cursor.fetchone()
        
    
    def update_member(self, member_id: int, data: dict):
        set_clause = ", ".join(f"{feild} = %s" for feild in data.keys())
        query = f"""
        UPDATE members
        SET
        {set_clause}
        WHERE id = %s
        """

        values = [val for val in data.values()]
        params = values + [member_id]

        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            db.conn.commit()
            return cursor.rowcount > 0
        
    def deactive_member(self, member_id: int):
        data = {"is_active": False}
        success = self.update_member(member_id, data)
        return success
    

    def activate_member(self, member_id: int):
        data = {"is_active": True}
        success = self.update_member(member_id, data)
        return success
    

    def increment_borrows(self, member_id: int):
        query = """
        UPDATE members
        SET
        total_borrows = total_borrows + 1
        WHERE id = %s
        """
        with db.conn.cursor() as cursor:
            cursor.execute(query, (member_id,))
            db.conn.commit()
            return cursor.rowcount > 0
        

    def count_active_members(self):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS active_members FROM members WHERE is_active = TRUE")
            return cursor.fetchall()[0]["active_members"]
        

    def get_top_member(self):
        logger.info("start getting top member...")
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("getting top total_borrows")
            cursor.execute("SELECT MAX(total_borrows) AS max_borrows FROM members")
            max_borrows = cursor.fetchone()["max_borrows"]
            logger.info("getting all members with top total_borrows")
            cursor.execute(f"SELECT id, total_borrows FROM members WHERE total_borrows = {max_borrows}")
            result = cursor.fetchall()
            logger.info("getting top_member complete")
            return result


        
    




member_manager = MemberDB()