pins_data = {
    # STOP
    0:[
        {"PIN":"NW_FW", "STATE":0},
        {"PIN":"NW_BW", "STATE":0},

        {"PIN":"NE_FW", "STATE":0},
        {"PIN":"NE_BW", "STATE":0},

        {"PIN":"SW_FW", "STATE":0},
        {"PIN":"SW_BW", "STATE":0},

        {"PIN":"SE_FW", "STATE":0},
        {"PIN":"SE_BW", "STATE":0},
    ],
    # FORWARD
    1:[
        {"PIN":"NW_FW", "STATE":1},
        {"PIN":"NW_BW", "STATE":0},

        {"PIN":"NE_FW", "STATE":1},
        {"PIN":"NE_BW", "STATE":0},

        {"PIN":"SW_FW", "STATE":1},
        {"PIN":"SW_BW", "STATE":0},

        {"PIN":"SE_FW", "STATE":1},
        {"PIN":"SE_BW", "STATE":0},
    ],
    # BACKWARD
    2:[
        {"PIN":"NW_FW", "STATE":0},
        {"PIN":"NW_BW", "STATE":1},

        {"PIN":"NE_FW", "STATE":0},
        {"PIN":"NE_BW", "STATE":1},

        {"PIN":"SW_FW", "STATE":0},
        {"PIN":"SW_BW", "STATE":1},

        {"PIN":"SE_FW", "STATE":0},
        {"PIN":"SE_BW", "STATE":1},
    ],
    # LEFT
    3:[
        {"PIN":"NW_FW", "STATE":0},
        {"PIN":"NW_BW", "STATE":1},

        {"PIN":"NE_FW", "STATE":1},
        {"PIN":"NE_BW", "STATE":0},

        {"PIN":"SW_FW", "STATE":1},
        {"PIN":"SW_BW", "STATE":0},

        {"PIN":"SE_FW", "STATE":0},
        {"PIN":"SE_BW", "STATE":1},
    ],
    # RIGHT
    4:[
        {"PIN":"NW_FW", "STATE":1},
        {"PIN":"NW_BW", "STATE":0},

        {"PIN":"NE_FW", "STATE":0},
        {"PIN":"NE_BW", "STATE":1},

        {"PIN":"SW_FW", "STATE":0},
        {"PIN":"SW_BW", "STATE":1},

        {"PIN":"SE_FW", "STATE":1},
        {"PIN":"SE_BW", "STATE":0},
    ],
    # TURNING LEFT
    5:[
        {"PIN":"NW_FW", "STATE":0},
        {"PIN":"NW_BW", "STATE":1},

        {"PIN":"NE_FW", "STATE":1},
        {"PIN":"NE_BW", "STATE":0},

        {"PIN":"SW_FW", "STATE":0},
        {"PIN":"SW_BW", "STATE":1},

        {"PIN":"SE_FW", "STATE":1},
        {"PIN":"SE_BW", "STATE":0},
    ],
    # TURNING RIGHT
    6:[
        {"PIN":"NW_FW", "STATE":1},
        {"PIN":"NW_BW", "STATE":0},

        {"PIN":"NE_FW", "STATE":0},
        {"PIN":"NE_BW", "STATE":1},

        {"PIN":"SW_FW", "STATE":1},
        {"PIN":"SW_BW", "STATE":0},

        {"PIN":"SE_FW", "STATE":0},
        {"PIN":"SE_BW", "STATE":1},
    ]
}

pwms_data= {
    0: [
        {"PIN":"NW_PWM","PWM":225},
        {"PIN":"NE_PWM","PWM":225},
        {"PIN":"SW_PWM","PWM":225},
        {"PIN":"SE_PWM","PWM":225}
    ],
} 
