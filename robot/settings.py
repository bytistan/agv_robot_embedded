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
        {"PIN":"NW_PWM","PWM":0},
        {"PIN":"NE_PWM","PWM":0},
        {"PIN":"SW_PWM","PWM":0},
        {"PIN":"SE_PWM","PWM":0}
    ],
    1: [
        {"PIN":"NW_PWM","PWM":225},
        {"PIN":"NE_PWM","PWM":225},
        {"PIN":"SW_PWM","PWM":225},
        {"PIN":"SE_PWM","PWM":225}
    ]
} 

destination_data = [
        {
            "area_name":"S1",
            "horizontal_coordinate":2250.0,
            "vertical_coordinate":0
        },
        {
            "area_name":"S2",
            "horizontal_coordinate":2250,
            "vertical_coordinate":3000
        },
        {
            "area_name":"A",
            "horizontal_coordinate":13250.0,
            "vertical_coordinate":6250.0
        },
        {
            "area_name":"B",
            "horizontal_coordinate":10625.0,
            "vertical_coordinate":6250.0,
        },
        {
            "area_name":"C",
            "horizontal_coordinate":5375.0,
            "vertical_coordinate":6250.0
        },
        {
            "area_name":"D",
            "horizontal_coordinate":2750.0,
            "vertical_coordinate":6250.0
        },
        {
            "area_name":"1",
            "horizontal_coordinate":0,
            "vertical_coordinate":0
        },
        {
            "area_name":"2",
            "horizontal_coordinate":0,
            "vertical_coordinate":12500.0
        },
        {
            "area_name":"3",
            "horizontal_coordinate":16000.0,
            "vertical_coordinate":12500.0
        },
        {
            "area_name":"4",
            "horizontal_coordinate":16000.0,
            "vertical_coordinate":0
        }
]
