from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from database.crud_service import CRUDService

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    db_session: Session = None

    @classmethod
    def set_db_session(cls, session: Session):
        cls.db_session = session

    @classmethod
    def create(cls, **kwargs):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.create(**kwargs)

    @classmethod
    def read(cls, instance_id: int):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.read(instance_id)

    @classmethod
    def update(cls, instance_id: int, **kwargs):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.update(instance_id, **kwargs)

    @classmethod
    def delete(cls, instance_id: int):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.delete(instance_id)

    @classmethod
    def filter(cls, *criterion):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.filter(*criterion)

    @classmethod
    def filter_one(cls, *criterion):
        crud_service = CRUDService(cls.db_session, cls)
        return crud_service.filter_one(*criterion)
