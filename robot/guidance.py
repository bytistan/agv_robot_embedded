class Guidance:
    def __init__(self,logger):
        self.logger = logger

    def control_passing_destination(self,location,destination):
        if location.direction in [0,1]:
            if (location.direction == 0 and location.horizontal_coordinate > destination.horizontal_coordinate) or (location.direction == 1 and location.horizontal_coordinate < destination.horizontal_coordinate):
                pass
        elif location.direction in [2,3]:
            if (location.direction == 2 and location.vertical_coordinate > destination.vertical_coordinate) or (location.direction == 3 and location.vertical_coordinate < destination.vertical_coordinate):
                pass 
        else:
            print("[+] Location direction is broken.")

    def check_turn_point(self,location,destination):
        if line_status in [1,2,3,4]:
            if location.direction in [0,1] and (destination.horizontal_coordinate + tolerance > location.horizontal_coordinate > destination.horizontal_coordinate - tolerance):
                pass # Make turn here 
            if location.direction in [2,3] and (destination.vertical_coordinate + tolerance > location.vertical_coordinate > destination.vertical_coordinate - tolerance):
                pass # Make turn here
        else:
            print("[+] Not suitable for line return.")

    def check(self,location,destination,line_status):
        try:

        except Exception as e:
            print(f"[-] Error occured: {e}") 

