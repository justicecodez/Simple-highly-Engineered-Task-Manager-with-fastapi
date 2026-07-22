from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException

class DBRepository:
    def __init__(self, db):
        self.db=db

    def check_if_value_exist(self, table, column, value)->bool:
        try:
            result=self.db.query(table).filter(column==value).first()
            if result:
                return result is not None
            return False
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")
        
    def create_record(self, record):
        try:
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")
        
    def get_record_by_value(self, table, column, value):
        try:
            record = self.db.query(table).filter(column == value).first()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
            return record
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

    def get_all_records(self, table, column, value):
        try:
            record = self.db.query(table).filter(column == value).all()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
            return record
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

    def update_record_by_id(self, update_data, record):
        try:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(record, key, value)
            self.db.commit()
            self.db.refresh(record)
            return record
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

    def delete_record_by_id(self, record):
            try:
                
                self.db.delete(record)
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")


