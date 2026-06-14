# Method	Endpoint	תיאור
# PATCH	/books/{id}/borrow/{member_id}	השאלת ספר לחבר
# PATCH	/books/{id}/return/{member_id}	החזרת ספר מחבר

from fastapi import APIRouter, HTTPException
from database.book_db import book_manager
from database.member_db import member_manager
from logs.logger_config import logger
router = APIRouter()

@router.get("")
def get_all_books():
    books = book_manager.get_all_books()
    if not books:
        logger.warning("There are no books in library!!!")
    return books

@router.post("", status_code=201)
def create_new_book(data: dict):
    logger.info("start creating book...")

    REQUIRED_FIELDS = ("title", "author", "genre")
    VALID_GENRES = ("Fiction", "Non-Fiction", "Science", "History", "Other")


    fields = set(data.keys())
    if fields != set(REQUIRED_FIELDS):
        logger.warning(f"fields must be {REQUIRED_FIELDS}")
        logger.error(f"could not create the book")
        raise HTTPException(422, detail=f"fields must be {REQUIRED_FIELDS}")
    
            
    if "genre" in data.keys():
        if data["genre"] not in VALID_GENRES:
            logger.warning(f"genre must be from {VALID_GENRES}")
            logger.error(f"could not create the book")
            raise HTTPException(422, detail=f"genre must be from {VALID_GENRES}")

    new_id =  book_manager.create_book(data)

    if not new_id:
        logger.error("could not create the book")
        raise HTTPException(500, detail={"msg": "internal server error, could not create the book"})
    
    logger.info(f"book {new_id} created successfully")
    return f"book {new_id} created successfully"


@router.get("/{book_id}")
def get_book_by_id(book_id: int):
    logger.info(f"start getting book {book_id}...")
    book = book_manager.get_book_by_id(book_id)
    if not book:
        logger.error(f"book {book_id} not found")
        raise HTTPException(404, detail=f"book {book_id} not found")
    logger.info(f"book {book_id} returned successfully")
    return book


@router.put("/{book_id}")
def update_book(book_id: int, data: dict):
    VALID_FEILDS = ("title", "author", "genre")
    for field in data.keys():
        if field not in VALID_FEILDS:
            raise HTTPException(422, detail=f"fields must be from {VALID_FEILDS}")
    
    VALID_GENRES = ("Fiction", "Non-Fiction", "Science", "History", "Other")
    if "genre" in data.keys():
        if data["genre"] not in VALID_GENRES:
            logger.warning(f"genre must be from {VALID_GENRES}")
            logger.error(f"could not create the book")
            raise HTTPException(422, detail=f"genre must be from {VALID_GENRES}")

    success = book_manager.update_book(book_id, data)
    if not success:
        logger.warning(f"book {book_id} is already up to date")
        logger.error(f"did not update book {book_id}")
        raise HTTPException(400, detail=f"book {book_id} is already up to date")

    return f"book {book_id} updated successfully"


@router.put("/{book_id}/borrow/{member_id}")
def borrow_book(book_id: int, member_id: int):
    """
    1. בדיקה שהספר קיים
    2. בדיקשה שהספר זמין
    3. בדיקה שהחבר קיים
    4. בדיקה שהחבר אקטיבי
    5. בדיקה שלחבר אין יותר מ3 ספרים
    6. השאלה.
    7. הוספת השאלה 1 לחבר
    """
    try:
        logger.info(f"start borrow book {book_id} by member {member_id}")
        book = book_manager.get_book_by_id(book_id)
        if not book:
            logger.warning(f"book {book_id} not found")
            raise HTTPException(404, detail=f"book {book_id} not found")
        
        is_available = book["is_available"]
        if not is_available:
            logger.warning(f"Book {book_id} is unavailable")
            raise HTTPException(400, f"book {book_id} is unavailable")
        
        member = member_manager.get_member_by_id(member_id)
        if not member:
            logger.warning(f"member {member_id} not found")
            raise HTTPException(404, detail=f"member {member_id} not found")
        
        is_active = member["is_active"]
        if not is_active:
            logger.warning(f"member {member_id} is not active")
            raise HTTPException(400,  detail=f"member {member_id} is not active")
        
        is_allow_to_borrow = book_manager.count_active_borrows_by_member(member_id)  < 3
        if not is_allow_to_borrow:
            logger.warning(f"member {member_id} has reached maximum books to borrow (3 books)")
            raise HTTPException(400, detail=f"member {member_id} has reached maximum books to borrow (3 books)")

        success = book_manager.set_available(book_id, False, member_id) 
        if not success:
            raise HTTPException(500,  detail="could not complete borrow")
        
        if member_manager.increment_borrows(member_id):
            logger.info(f"add 1 to total_borrows of member {member_id}")
        logger.info(f"member {member_id} borrowed book {book_id} successfully")
        return f"member {member_id} borrowed book {book_id} successfully"
    
    except HTTPException as e:
        logger.error("could not complete borrow")
        if e.status_code == 400:
            return e.detail
        raise

