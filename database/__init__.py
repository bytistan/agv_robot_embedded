from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")

Session = sessionmaker(bind=engine)
db_session = Session()
