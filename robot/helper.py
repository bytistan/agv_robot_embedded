from database import engine 
from sqlalchemy.orm import sessionmaker
from models import *

def set_mission(robot,data):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        active_mission = session.query(Mission).filter(Mission.is_active == True).first()
        any_active_mission = False if active_mission else True 

        mission = Mission(robot_id = robot.id,is_active = any_active_mission)

        session.add(mission) 
        session.flush()

        for road_map in data:
            qr_code = session.query(QRCode).filter(QRCode.area_name==road_map.get("area_name")).first()

            if not qr_code:
                print("[!] Qr not found.") 
                return None

            rm = RoadMap(
                mission_id = mission.id,
                qr_code_id = qr_code.id,
                index = road_map.get("index")
            )
                                            
            session.add(rm)
                    
        session.commit()
        session.close()
    except Exception as e:
        session.close()
        print(f"[-] Error occured: {e}") 

def get_connection():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        connection = session.query(Connection).filter(Connection.id > 0).first()

        if connection:
            print("[+] Connection record found.")
            return connection 
        else:
            print("[-] No connection record found in database .")

        session.close()
    except Exception as e:
        session.close()
        print(f"[-] Error occured: {e}") 

def close_mission(mission):
    # Function Explanation : Basicly update the mission value.
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        mission.is_active = False 

        session.commit()
        session.close()

        print("[+] Robot reached the destination.") 
    except Exception as e:
        session.close()
        print(f"[-] Error occured: {e}.") 

def get_destination(mission):
    # Function Explanation : Simply put, it finds the target qr code through index numbers.
    try:
        destination = None
        for road_map in mission.road_map:
            if not destination:
                destination = road_map
            if road_map.index < target.index and not road_map.reached:
                destination = road_map
        return destination 
    except Exception as e:
        print(f"[-] Error occured: {e}.") 

def get_robot():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Just have one robot record in database and need the find.
        robot = session.query(Robot).filter(Robot.id > 0).first()

        if robot:
            print("[+] Robot record found.")
            return robot
        else:
            print("[!] No record found in database robot.")

        session.close()
    except Exception as e:
        session.close()
        print(f"[-] Error occured: {e}") 

def get_location():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Just have one location record in database and need the find.
        location = session.query(Location).filter(Location.id > 0).first()

        if location:
            print("[+] Location record found.")
            return location 
        else:
            print("[!] Location record is not found.")

        session.close()
    except Exception as e:
        session.close()
        print(f"[-] Error occured: {e}") 
