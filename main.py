from robot.network.robot_client import RobotClient

from network import url, auth_data 
from system_startup import SystemStartup

if __name__ == "__main__":
    # Default things  
    system_startup = SystemStartup()
    
    # We listen the mission
    client = RobotClient(auth_data)
    client.start(url)
