# Method	Endpoint	תיאור
# GET	/reports/summary	דוח כללי
# GET	/reports/books-by-genre	ספרים לפי ז'אנר
# GET	/reports/top-member	החבר הכי פעיל


from fastapi import APIRouter
from database.book_db import book_manager
from database.member_db import member_manager
from logs.logger_config import logger

router = APIRouter()

@router.get("/summary")
def get_summary():
    """
    מציג את המספר של: :
    1. כל הספרים בספריה
    2. כל הספרים הזמינים להשאלה
    3. כל הספרים המושאלים
    4. כל החברים הפעילים
    """
    logger.info("start creating summary report...")
    all_books = book_manager.count_all_books()
    available_books = book_manager.count_available_books()
    borrowed_books = all_books - available_books
    active_members = member_manager.count_active_members()
    logger.info("summary report completed")
    return {
        "all_books": all_books, 
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "active_members": active_members 
            }

@router.get("/books-by-genre")
def report_book_by_genre():
    return book_manager.count_by_genre()


@router.get("/top-member")
def report_top_member():
    return member_manager.get_top_member()



    