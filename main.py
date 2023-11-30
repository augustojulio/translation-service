from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.openapi.models import *
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Word

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Words translation API",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # app.include_router(api_router)

    add_pagination(app)

    return app


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/word/{word}")
async def get_word_details(word: str, include_definitions: bool = False, include_synonyms: bool = False, include_translations: bool = False, db: Session = Depends(get_db)):
    # Check if word is in the database
    db_word = db.query(Word).filter(Word.word == word).first()

    if db_word is None:
        # Fetch data from Google Translate (implement this part)
        # For now, let's assume the data is retrieved and save it to the database
        new_word = Word(word=word, definitions="Definition", synonyms="Synonyms", translations="Translations", examples="Examples")
        db.add(new_word)
        db.commit()
        db.refresh(new_word)
        db_word = new_word

    # Return the word details
    return {
        "word": db_word.word,
        "definitions": db_word.definitions if include_definitions else None,
        "synonyms": db_word.synonyms if include_synonyms else None,
        "translations": db_word.translations if include_translations else None,
        "examples": db_word.examples if include_definitions else None,
    }
    
@app.get("/words/")
async def get_words_list(page: int = 1, per_page: int = 10, sort_by: str = "word", filter_word: str = None, db: Session = Depends(get_db)):
    # Retrieve words from the database with pagination, sorting, and filtering
    query = db.query(Word)

    # Apply filtering
    if filter_word:
        query = query.filter(Word.word.ilike(f"%{filter_word}%"))

    # Apply sorting
    if sort_by == "word":
        query = query.order_by(Word.word)

    # Apply pagination
    words = query.offset((page - 1) * per_page).limit(per_page).all()

    return words

@app.delete("/word/{word}")
async def delete_word(word: str, db: Session = Depends(get_db)):
    # Delete the word from the database
    db_word = db.query(Word).filter(Word.word == word).first()

    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    db.delete(db_word)
    db.commit()

    return {"message": f"Word '{word}' deleted successfully"}