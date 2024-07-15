from database import db_session 
from termcolor import colored

from models import *
from datetime import datetime 

def mission_completed(mission_id):
    try:
        if mission_id is None: 
            print(colored(f"[WARN] The mission id parameter is null.", "yellow", attrs=["bold"]))
            return 
        
        mission = db_session.query(Mission).filter(Mission.id == mission_id).first()

        mission.completed = True
        mission.is_active = False 

        mission.end_time = datetime.now() 

        db_session.add(mission)
        db_session.commit()
        
    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[MISSION_COMPLETED]", "red", attrs=["bold"]))

def road_map_reached(road_map_id):
    try:
        if road_map_id is None: 
            print(colored(f"[WARN] The road map_id parameter is null.", "yellow", attrs=["bold"]))
            return 
        
        road_map = db_session.query(RoadMap).filter(RoadMap.id == road_map_id).first()
        road_map.reached = True

        db_session.add(road_map)
        db_session.commit()

    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[ROAD_MAP_REACHED]", "red", attrs=["bold"]))

def find_road_map(mission_id):
    try:
        road_maps = db_session.query(RoadMap).filter(RoadMap.mission_id == mission_id).all()

        if not road_maps: 
            print(colored(f"[WARN] Road map not found.", "yellow", attrs=["bold"]))
            return
        
        r = None 
        for road_map in road_maps:
            if r is None and not road_map.reached:
                r = road_map 
            if r and road_map.index < r.index:
                    r = road_map 
        
        if r is None:
            print(colored(f"[WARN] Road map not found.", "yellow", attrs=["bold"]))
            return

        qr_code  = db_session.query(QRCode).filter(QRCode.id == r.qr_code_id).first()
        
        if not qr_code:
            print(colored(f"[WARN] Road map found but qr code not found.", "yellow", attrs=["bold"]))
            return 

        data = {
            "id":r.id,
            "qr_code": {
                "area_name":qr_code.area_name,
                "horizontal_coordinate":qr_code.horizontal_coordinate,
                "vertical_coordinate":qr_code.vertical_coordinate
            }
        }

        print(colored(f"[INFO] Target : {qr_code.area_name}, [COR] {qr_code.vertical_coordinate}:{qr_code.horizontal_coordinate}.", "yellow", attrs=["bold"]))

        return data

    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[FIND_ROAD_MAP]", "red", attrs=["bold"]))

def save_qr(robot_id,data):
    try:
        is_qr_code = db_session.query(QRCode).filter(QRCode.area_name == data.get("area_name")).first()
        flag = False if is_qr_code else True 

        if flag:
            qr_code = QRCode(
                robot_id = robot_id,
                vertical_coordinate = data.get("vertical_coordinate"),
                horizontal_coordinate = data.get("horizontal_coordinate"),
                area_name = data.get("area_name")
            )

            db_session.add(qr_code)
            db_session.commit()

    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[SAVE_QR]", "red", attrs=["bold"]))

def set_mission(robot_id, data):
    try:
        active_mission = db_session.query(Mission).filter(Mission.is_active == True).first()
        any_active_mission = False if active_mission else True 

        mission = Mission(robot_id = robot_id,is_active = any_active_mission)

        db_session.add(mission) 
        db_session.flush()

        for road_map in data:
            qr_code = db_session.query(QRCode).filter(QRCode.area_name==road_map.get("area_name")).first()

            if not qr_code:
                print(colored("[WARN] Qr record not found.", "yellow", attrs=["bold"]))
                return None

            rm = RoadMap(
                mission_id = mission.id,
                qr_code_id = qr_code.id,
                index = road_map.get("index")
            )
                                            
            db_session.add(rm)
        
        db_session.commit()

        print(colored(f"[INFO] Mission saved to database.", "green", attrs=["bold"]))
        return mission.id 
    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[SET_MISSION]", "red", attrs=["bold"]))

def get_connection():
    try:
        connection = db_session.query(Connection).filter(Connection.id > 0).first()

        if connection:
            print(colored("[INFO] Connection record found.", "green", attrs=["bold"]))
            return connection 
        else:
            print(colored("[WARN] No connection record found in database.", "yellow", attrs=["bold"]))

    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[GET_CONNECTION]", "red", attrs=["bold"]))

def close_mission(mission_id, complated):
    # Function Explanation : Basicly update the mission value.
    try:
        mission = Mission(id=mission_id)
        mission.is_active = False 

        db_session.commit()

        print(colored(f"[INFO] Robot reached the destination.", "green", attrs=["bold"]))
    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[CLOSE_MISSION]", "red", attrs=["bold"]))

def get_robot():
    try:
        # Just have one robot record in database and need the find.
        robot = db_session.query(Robot).filter(Robot.id > 0).first()

        if robot:
            print(colored("[INFO] Robot record found.", "green", attrs=["bold"]))
            return {
                "serial_number":robot.serial_number,
                "id":robot.id
            }
        else:
            print(colored("[WARN] Robot record is not found.", "yellow", attrs=["bold"])) 

    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[GET_ROBOT]", "red", attrs=["bold"]))

def get_location():
    try:
        # Just have one location record in database and need the find.
        location = db_session.query(Location).filter(Location.id > 0).first()

        if location:
            print(colored("[INFO] Location record found.", "green", attrs=["bold"]))
            return location 
        else:
            print(colored("[WARN] Location record is not found.", "yellow", attrs=["bold"]))

        db_session.close()
    except Exception as e:
        db_session.close()
        print(colored(f"[ERR] {e} -> [HELPER]:[GET_LOCATION]", "red", attrs=["bold"]))
