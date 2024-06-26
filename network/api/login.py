import requests
from network import url,auth_data
from . import login_url

from database import engine 
from sqlalchemy.orm import sessionmaker
from models.connection import Connection

from logger import logger
from datetime import datetime 

def login():
    try:
        # Try to login with serial number and secret key
        response = requests.post(login_url ,json=auth_data)
        
        # If successfuly connect to server achive jwt token, this using for future data transfer 
        if response.status_code == 200:
            token = response.json().get("access_token")

            if token is not None:
                logger.info(f"JWT Token: {token}")

                Session = sessionmaker(bind=engine)
                session = Session()
                
                connection = session.query(Connection).filter(Connection.id > 0).first()
                if connection is None:
                    # If connection data is not created create one :)
                    connection = Connection(token=token)
                    session.add(connection)
                else:
                    # Update token to database if connection data is already created
                    connection.token = token
                    connection.updated_date = datetime.utcnow()
                session.commit()
                session.close()

                # Return the token but this one is not important because we will use in database.
                return token
            else:
                logger.warning("Connection is succesfully but server is not return token.")
        else:
            logger.error(f"Error occured : {response.json()}")
    except Exception as e:
        logger.error(f"Error occured : {e}")
