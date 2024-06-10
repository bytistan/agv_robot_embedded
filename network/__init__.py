import socketio
from helper.json_helper import read_json

url = "http://192.168.1.106:5000"

sio = socketio.Client()

auth_data = read_json("./network/auth.json")

# Function end socket naming rules (assuming direct room name as event name)
# This section defines the naming conventions for your socket functions.
# Events are named directly with the room name (e.g., 01 for room 0_1).

# Room syntax explanation
# The room name consists of two parts separated by an underscore (_):

"""
Room Name Structure:

- The first part (before the underscore) indicates the role of the participants:
  - 0: Room for human users
  - 1: Room for robots
- The second part (after the underscore) specifies the action:
  - 0: Room for participants leaving an activity
  - 1: Room for participants joining an activity
"""

# Controller syntax explanation
# The numeric codes likely serve as identifiers within your controller logic:

"""
Controller Codes:

- 0: Refers to actions related to location data
- 1: Refers to actions related to missions or tasks
- 2: Refers to actions related to QR codes
- 3: Refers to actions related to status updates
- 4: Refers to actions related to turn points (possibly for navigation)
"""
