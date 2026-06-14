from fastapi import FastAPI
from routes.book_routes import router as books_router

app = FastAPI()

app.include_router(books_router, prefix="/books")