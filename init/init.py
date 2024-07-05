from database import engine
from helper.json_helper import read_json
from helper.security import generate_secret_key
from models.robot import Robot
from sqlalchemy.orm import sessionmaker

def init_():
    data = read_json("./init/init.json").get("robot")

    Session = sessionmaker(bind=engine)
    session = Session()

    filtered_robot = session.query(Robot).filter(Robot.serial_number == data.get("serial_number")).first()

    if not filtered_robot:
        robot = Robot(serial_number=data.get("serial_number"),mode=data.get("mode"),secret_key=data.get("secret_key"))

        session.add(robot)
        session.commit()

    session.close()
