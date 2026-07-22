from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.mysql import get_db
from app.repository.app_repository import DBRepository


def get_db_repository(db: Session = Depends(get_db)):
    return DBRepository(db)