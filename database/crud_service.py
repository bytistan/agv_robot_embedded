from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import and_

from . import * 

from termcolor import colored
import traceback

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
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def read(self, instance_id: int):
        try:
            instance = self.db_session.query(self.model).get(instance_id)
            if instance is None:
                print(colored(f"[WARN] Instance with id {instance_id} not found.", "yellow", attrs=["bold"]))
            return instance
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

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
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def delete(self, instance_id: int):
        try:
            instance = self.db_session.query(self.model).get(instance_id)
            if instance is None:
                print(colored(f"[WARN] Instance with id {instance_id} not found.", "yellow", attrs=["bold"]))
                return False

            self.db_session.delete(instance)
            self.db_session.commit()
            return True
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def filter(self, *criterion):
        try:
            query = self.db_session.query(self.model).filter(and_(*criterion))
            return query.all()
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def filter_one(self, *criterion):
        try:
            query = self.db_session.query(self.model).filter(and_(*criterion))
            return query.first()
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
