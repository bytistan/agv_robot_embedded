from robot.robot_client import RobotClient

from network import url, auth_data 
from system_startup import SystemStartup

if __name__ == "__main__":
    system_startup = SystemStartup()

    client = RobotClient(auth_data)
    client.start(url)
