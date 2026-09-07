import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

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