from fastapi import FastAPI, exception_handlers, Request, HTTPException
from database.db_connection import db
from routes.book_routes import router as books_router
from routes.member_routes import router as members_router
from routes.report_routes import router as reports_router
from contextlib import asynccontextmanager
from mysql.connector import Error as MYSQL_ERROR
from logs.logger_config import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.conn = db.get_connection()

    yield

    db.close()



app = FastAPI(lifespan= lifespan)

@app.exception_handlers(MYSQL_ERROR)
def sql_errors(req: Request, e: MYSQL_ERROR):
    logger.error(f"mysql error, request: {req.url}, exeption: {e.msg}")        
    raise HTTPException(500, "internal error")

app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(members_router, prefix="/members", tags=["members"])
app.include_router(reports_router, prefix ="/reports", tags=["reports"])


