cont_data = {
    # STOP
    0:{ 
        "PINS":[
            {"PIN":"NW_FW", "STATE":0},
            {"PIN":"NW_BW", "STATE":0},

            {"PIN":"NE_FW", "STATE":0},
            {"PIN":"NE_BW", "STATE":0},

            {"PIN":"SW_FW", "STATE":0},
            {"PIN":"SW_BW", "STATE":0},

            {"PIN":"SE_FW", "STATE":0},
            {"PIN":"SE_BW", "STATE":0},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":0},
            {"PIN":"NE_PWM","PWM":0},
            {"PIN":"SW_PWM","PWM":0},
            {"PIN":"SE_PWM","PWM":0}
        ]
    },
    # FORWARD
    1:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":1},
            {"PIN":"NW_BW", "STATE":0},

            {"PIN":"NE_FW", "STATE":1},
            {"PIN":"NE_BW", "STATE":0},

            {"PIN":"SW_FW", "STATE":1},
            {"PIN":"SW_BW", "STATE":0},

            {"PIN":"SE_FW", "STATE":1},
            {"PIN":"SE_BW", "STATE":0},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    },
    # BACKWARD
    2:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":0},
            {"PIN":"NW_BW", "STATE":1},

            {"PIN":"NE_FW", "STATE":0},
            {"PIN":"NE_BW", "STATE":1},

            {"PIN":"SW_FW", "STATE":0},
            {"PIN":"SW_BW", "STATE":1},

            {"PIN":"SE_FW", "STATE":0},
            {"PIN":"SE_BW", "STATE":1},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    },
    # LEFT
    3:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":0},
            {"PIN":"NW_BW", "STATE":1},

            {"PIN":"NE_FW", "STATE":1},
            {"PIN":"NE_BW", "STATE":0},

            {"PIN":"SW_FW", "STATE":1},
            {"PIN":"SW_BW", "STATE":0},

            {"PIN":"SE_FW", "STATE":0},
            {"PIN":"SE_BW", "STATE":1},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    },
    # RIGHT
    4:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":1},
            {"PIN":"NW_BW", "STATE":0},

            {"PIN":"NE_FW", "STATE":0},
            {"PIN":"NE_BW", "STATE":1},

            {"PIN":"SW_FW", "STATE":0},
            {"PIN":"SW_BW", "STATE":1},

            {"PIN":"SE_FW", "STATE":1},
            {"PIN":"SE_BW", "STATE":0},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    },
    # TURNING LEFT
    5:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":0},
            {"PIN":"NW_BW", "STATE":1},

            {"PIN":"NE_FW", "STATE":1},
            {"PIN":"NE_BW", "STATE":0},

            {"PIN":"SW_FW", "STATE":0},
            {"PIN":"SW_BW", "STATE":1},

            {"PIN":"SE_FW", "STATE":1},
            {"PIN":"SE_BW", "STATE":0},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    },
    # TURNING RIGHT
    6:{
        "PINS":[
            {"PIN":"NW_FW", "STATE":1},
            {"PIN":"NW_BW", "STATE":0},

            {"PIN":"NE_FW", "STATE":0},
            {"PIN":"NE_BW", "STATE":1},

            {"PIN":"SW_FW", "STATE":1},
            {"PIN":"SW_BW", "STATE":0},

            {"PIN":"SE_FW", "STATE":0},
            {"PIN":"SE_BW", "STATE":1},
        ],
        "PWM":[
            {"PIN":"NW_PWM","PWM":225},
            {"PIN":"NE_PWM","PWM":225},
            {"PIN":"SW_PWM","PWM":225},
            {"PIN":"SE_PWM","PWM":225}
        ]
    } 
}

