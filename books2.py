from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2025)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Author Name',
                'description': 'Book Description',
                'rating': 5,
                'published_date': 2012
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'CodingWithRoby', 'A very nice book!', 5, 2016),
    Book(2, 'Be Fast with FastAPI', 'CodingWithRoby', 'A great book!', 5, 2017),
    Book(3, 'Master Endpoints', 'CodingWithRoby', 'An awesome book!', 5, 2018),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2021),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2017),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2021)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item Not Found')

@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_book(book_rating: int = Query(gt=0, lt=6)):
    book_list = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_list.append(book)
    return book_list

@app.get('/books/year/', status_code=status.HTTP_200_OK)
async def read_book_year(published_year: int = Query(gt=1999, lt=2025)):
    book_list =[]
    for i in range(len((BOOKS))):
        if BOOKS[i].published_date == published_year:
            book_list.append(BOOKS[i])
    return book_list
@app.post('/create_book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    print(type(book_request))
    new_book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    # book.id = BOOKS[-1].id + 1
    # else:
    # book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not Found')

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not Found')


