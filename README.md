# library_test


ניהול ספרייה, על ידי ניהול המשתמשים, ניהול הספרים והחיבורים שביניהם.
המערכת מנוהלת באופן של לקוח - שרת.

### יצירת קונטיינר של mysql:
```
docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8
```
```text
library-api/
│
│
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
|   |__ logger_config.py
│
├── README.md
├── requirements.txt
└── .gitignore
```


## TABLES
#### BOOKS

| שדה | הסבר |
|-----|-------|
|id | המזהה של הספר|
|title | השם של הספר|
|author | מחבר הספר |
|genre | Fiction , Non-Fiction , Science , History , Other|
|is_available | האם הספר זמין להשאלה או שהוא כבר מושאל |
|borrowed_by_member_id | מזהה החבר שמחזיק את הספר |

#### MEMBERS

| שדה | הסבר |
|-----|------|
| id | מפתח ראשי |
| name | שם החבר |
| email | כתובת מייל |
| is_active | האם החבר פעיל (אם לא הוא לא יכול לשאול ספר) |
| total_borrows | מונה סך הכל השאלות |
***
<br>
<br><br>
<br>
<br><br>



## חוקי מערכת
| חוק | נושא | הכלל |
|-----|-------|------|
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה is_available=True, borrowed_by=NULL | 
| 2 | ז'אנר | Fiction / Non-Fiction / Science / History / Other — אחרת - מחזיר שגיאה | 
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה is_active=True total_borrows=0 |
| 4 | מייל | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם is_active=False — אי אפשר להשאיל ספר |
| 6 | ספר ללא זמין | אי אפשר להשאיל ספר שכבר מושאל (is_available=False) | 
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

---
<br><br><br><br><br><br>



# Endpoints
<br>

## Books

| Method | Endpoint| תיאור|
| ------ | ------- | ----- |
| POST   | /books | יצירת ספר |
| GET    | /books | כל הספרים|
| GET    | /books/{id}| ספר לפי ID |
| PATCH  | /books/{id}| עדכון ספר |
| PATCH  | /books/{id}/borrow/{member_id} | השאלת ספר לחבר |
| PATCH  | /books/{id}/return/{member_id} | החזרת ספר מחבר |
___
<br><br>
## Members

| Method | Endpoint | תיאור|
| ------ | -------- | ------ |
| POST   | /members  | יצירת חבר  |
| GET    | /members  | כל החברים  |
| GET    | /members/{id} | חבר לפי ID |
| PATCH  | /members/{id} | עדכון חבר  |
| PATCH  | /members/{id}/deactivate | השבתת חבר  |
| PATCH  | /members/{id}/activate | הפעלת חבר |
___
<br><br>
## Reports

| Method | Endpoint | תיאור|
| ------ | -------- | ------ |
| GET | /reports/summary | דוח כללי|
| GET | /reports/books-by-genre | ספרים לפי ז'אנר |
| GET | /reports/top-member | החבר הכי פעיל|



<br><br>
 ## זרימת המערכת
```
                                              (main) השרת מוקם
                                                      |
                                נוצר חיבור לקונטיינר ולדאטה-בייס (db_connection)
                                                      |
                                                משתמש שולח בקשה
        |                                             |                                                |
    בקשר לספרים                                   בקשר לחברים                                  בקשר לדוחות
        |                                             |                                                |
מופעל הנתיב המתאים (report_routes)    מופעל הנתיב המתאים (members_routes)           מופעל הנתיב המתאים (books_routes)
        |                                             |                                                |
פעולה בטבלת הנתונים                            פעולה בטבלת הנתונים                          פעולה בטבלת הנתונים
(book_db, members_db)                           (members_db)                                       (books_db)
        |                                             |                                                |
(main)החזרת תשובה למשתמש                 (main)החזרת תשובה למשתמש                         (main)החזרת תשובה למשתמש
```


## הוראות הרצה
```
pip install -r requirements.txt
uvicorn main:app
```