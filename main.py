from fastapi import FastAPI
from routes.book_routes import router as books_router
from routes.member_routes import router as members_router
from routes.report_routes import router as reports_router

app = FastAPI()

app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(members_router, prefix="/members", tags=["members"])
app.include_router(reports_router, prefix ="/reports", tags=["reports"])
