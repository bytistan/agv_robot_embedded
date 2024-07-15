from database import engine

from helper.json_helper import read_json
from helper.security import generate_secret_key
from termcolor import colored
from sqlalchemy.orm import sessionmaker

from models.robot import Robot
from models.qr_code import QRCode

from . import DEFAULT_QR


def init_default_qr():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        robot = session.query(Robot).filter(Robot.id > 0).first()

        for qr in DEFAULT_QR:
            if not session.query(QRCode).filter(QRCode.area_name==qr.get("area_name")).first():
                session.add(QRCode(
                    robot_id = robot.id,
                    vertical_coordinate = qr.get("vertical_coordinate"),
                    horizontal_coordinate = qr.get("horizontal_coordinate"),
                    area_name = qr.get("area_name")
                ))

        session.commit()
        session.close()

    except Exception as e:
        session.close()
        print(colored(f"[ERR] {e}", "red" ,attrs=["bold"]))

def init_():
    try:
        data = read_json("./init/init.json").get("robot")

        Session = sessionmaker(bind=engine)
        session = Session()

        filtered_robot = session.query(Robot).filter(Robot.serial_number == data.get("serial_number")).first()

        if not filtered_robot:
            robot = Robot(serial_number=data.get("serial_number"),mode=data.get("mode"),secret_key=data.get("secret_key"))

            session.add(robot)
            session.commit()

        session.close()

    except Exception as e:
        session.close()
        print(colored(f"[ERR] {e}", "red" ,attrs=["bold"]))
