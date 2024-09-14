from database import db_session

from helper.json_helper import read_json
from helper.security import generate_secret_key
from termcolor import colored

from models.robot import Robot
from models.qr_code import QRCode

def init_():
    try:
        data = read_json("./init/init.json").get("robot")

        filtered_robot = db_session.query(Robot).filter(Robot.serial_number == data.get("serial_number")).first()

        if not filtered_robot:
            robot = Robot(serial_number=data.get("serial_number"),mode=data.get("mode"),secret_key=data.get("secret_key"))

            db_session.add(robot)
            db_session.commit()
    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e}", "red" ,attrs=["bold"]))
