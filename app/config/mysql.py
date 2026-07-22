from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings.database import database


DB_URL=f"mysql+pymysql://{database.DB_USER}:{database.DB_PASSWORD}@{database.DB_HOST}:{database.DB_PORT}/{database.DB_NAME}"
engine=create_engine(DB_URL)

sessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()