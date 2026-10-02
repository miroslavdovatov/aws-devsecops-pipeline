import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL
            );
        """))
        connection.commit()

@app.get("/health")
def health_check():
    """Pipeline uses this to verify the app is operational."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/api/data")
def read_data():
    """Queries PostgreSQL and returns sample data."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'PostgreSQL is connected and returning data' AS message"))
            row = result.fetchone()
            return {"status": "success", "data": row[0]}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch data from database")

@app.post("/notes")
def create_note(content: str):
    try:
        with engine.connect() as connection:
            connection.execute(
                text("INSERT INTO notes (content) VALUES (:content)"),
                {"content": content}
            )
            connection.commit()
        return {"status": "success", "added": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes")
def get_notes():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT content FROM notes"))
            notes = [row[0] for row in result.fetchall()]
        return {"notes": notes}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch notes")