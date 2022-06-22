from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import BookSchema, RequestBook, Response
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create(request: RequestBook, db: Session = Depends(get_db)):
    crud.create_book(db, request.parameter)
    return Response(code=200, status='ok', message="Book created successfully").dict(exclude_none=None)


@router.get("/")
async def get(db: Session = Depends(get_db)):
    _book = crud.get_book(db, 0, 100)
    return Response(code=200, status="ok", message="Success Fetch all data", result=_book).dict(exclude_none=True)


@router.get("/{id}")
async def get_by_id(id: int, db: Session = Depends(get_db)):
    _book = crud.get_book_by_id(db, id)
    return Response(code=200, status="ok", message="Success get data", result=_book).dict(exclude_none=True)


@router.put("/{id}")
async def update_book(request: RequestBook, db: Session = Depends(get_db)):
    _book = crud.update_book(db, book_id=request.parameter.id,
                             title=request.parameter.title,
                             description=request.parameter.description)
    if _book:
        return Response(code=200, status="ok", message="Success update data", result=_book)
    else:
        return Response(code=404, status="ok", message="Invalid Book ID ", result=_book)


@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    _book = crud.remove_book(db, book_id=id)
    if _book:
        return Response(code=200, status="ok", message="Success delete data")
    else:
        return Response(code=404, status="ok", message="Invalid Book ID")