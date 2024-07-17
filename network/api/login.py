import requests

from datetime import datetime 
from termcolor import colored
from sqlalchemy.orm import sessionmaker

from network import url,auth_data
from . import login_url

from database import db_session 
from models.connection import Connection

def login():
    try:
        # Try to login with serial number and secret key
        response = requests.post(login_url ,json=auth_data)
        
        # If successfuly connect to server achive jwt token, this using for future data transfer 
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(colored("[INFO] Login to server.", "green", attrs=["bold"]))
            if token is not None:
                connection = db_session.query(Connection).filter(Connection.id > 0).first()
                if connection is None:
                    # If connection data is not created create one :)
                    connection = Connection(token=token)
                    db_session.add(connection)
                else:
                    # Update token to database if connection data is already created
                    connection.token = token
                    connection.updated_date = datetime.utcnow()

                print(colored("[INFO] JWT token saved to local database.", "green", attrs=["bold"]))

                db_session.commit()

                # Return the token but this one is not important because we will use in database.
                return token
            else:
                print(colored("[WARN] Connection is succesfully but server is not return token.", "yellow" ,attrs=["bold"]))
        else:
            print(colored(f"[ERR] {response.json()}", "red" ,attrs=["bold"]))
    except Exception as e:
        db_session.close()
        print(colored(f"Error occured : {e}", "red" ,attrs=["bold"]))
