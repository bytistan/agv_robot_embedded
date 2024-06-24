from database import engine 
from sqlalchemy.orm import sessionmaker

def close_mission(mission):
    """
        Function Explanation : Basicly update the mission value.
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        mission.is_active = False 
        session.commit()

        logger.info("Robot reached the destination") 
    except Exception as e:
        logger.error(f"Error occured: {e}") 
    finally:
        if session is not None:
            session.close()

def get_destination(mission):
    """
        Function Explanation : Simply put, it finds the target qr code through index numbers.
    """
    try:
        destination = None
        for road_map in mission.road_map:
            if not destination:
                destination = road_map
            if road_map.index < target.index and not road_map.reached:
                destination = road_map
        return destination 
    except Exception as e:
        logger.error(f"Error occured: {e}") 

def get_robot():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Just have one robot record in database and need the find.
        robot = session.query(Robot).filter(Robot.id > 0).first()

        if robot:
            logger.info("Robot record found.")
            return robot
        else:
            logger.warning("No record found in database robot.")
    except Exception as e:
        logger.error(f"Error occured: {e}") 
    finally:
        if session is not None:
            session.close()

def get_location():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Just have one location record in database and need the find.
        location = session.query(Location).filter(Location.id > 0).first()

        if location:
            logger.info("Location record found.")
            return location 
        else:
            logger.warning("Location record is not found.")
    except Exception as e:
        logger.error(f"Error occured: {e}") 
    finally:
        if session is not None:
            session.close()
