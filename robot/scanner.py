from database import engine 
from sqlalchemy.orm import sessionmaker

from pyzbar.pyzbar import decode
from .helper import get_destination

class Scanner:
    def __init__(self,logger):
        self.logger = logger

    def scan(self,image,destination):

        try:
            return decode(image) 
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 

    def check(self,image,destination,mission):

        try:
            result = self.scan(image)
            Session = sessionmaker(bind=engine)
            session = Session()
 
            area_name = scan_result[0].data.encode("utf-8") 

            # If scan result same with the destination area.
            if area_name == destination.qr_code.area_name:
                self.logger.info(f"Robot reached the {area_name} destination") 
                # Update the destination column reached.
                destination.reached = True
                session.commit()
                # Find new destination.
                destination = get_destination(mission)
                # If find the new destination it is good.
                if destination:
                    session.close()
                    return destination
                    self.logger.info("Destination updated.")
                else:
                    # If not find new destination this means the mission is over.
                    self.logger.info("Destination record not found.")
            else:
                self.logger.info(f"{area_name} is not the destination area.")

            session.close()
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
