from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import and_

from . import * 

class CRUDService:
    def __init__(self, db_session: Session, model):
        self.db_session = db_session
        self.model = model

    def create(self, **kwargs):
        try:
            instance = self.model(**kwargs)
            self.db_session.add(instance)
            self.db_session.commit()
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
            return None

    def read(self, instance_id: int):
        try:
            instance = self.db_session.query(self.model).get(instance_id)
            if instance is None:
                print(colored(f"[WARN] Instance with id {instance_id} not found.", "yellow", attrs=["bold"]))
            return instance
        except SQLAlchemyError as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
            return None

    def update(self, instance_id: int, **kwargs):
        try:
            instance = self.db_session.query(self.model).get(instance_id)
            if instance is None:
                print(colored(f"[WARN] Instance with id {instance_id} not found.", "yellow", attrs=["bold"]))
                return None

            for key, value in kwargs.items():
                setattr(instance, key, value)

            self.db_session.commit()
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
            return None

    def delete(self, instance_id: int):
        try:
            instance = self.db_session.query(self.model).get(instance_id)
            if instance is None:
                print(colored(f"[WARN] Instance with id {instance_id} not found.", "yellow", attrs=["bold"]))
                return False

            self.db_session.delete(instance)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
            return False

    def filter(self, *criterion):
        try:
            query = self.db_session.query(self.model).filter(and_(*criterion))
            return query.all()
        except SQLAlchemyError as e:
            print(colored(f"[ERR] {e} -> [HELPER]:[FILTER]", "red", attrs=["bold"]))
            return None

    def filter_one(self, *criterion):
        try:
            query = self.db_session.query(self.model).filter(and_(*criterion))
            return query.first()
        except SQLAlchemyError as e:
            print(colored(f"[ERR] {e} -> [HELPER]:[FILTER_ONE]", "red", attrs=["bold"]))
            return None
