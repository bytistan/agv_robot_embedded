import os 

class Focuser:
    I2C_BUS = 9 
    CHIP_I2C_ADDR = 0x0C
    OPT_BASE    = 0x1000
    OPT_FOCUS   = OPT_BASE | 0x01
    opts = {
        OPT_FOCUS : {
            "MIN_VALUE": 0,
            "MAX_VALUE": 1000,
            "DEF_VALUE": 0,
        }
    }

    def __init__(self):
        self.focus_value = 0
        
    def read(self):
        return self.focus_value

    def write(self, chip_addr, value):
        if value < 0:
            value = 0
        self.focus_value = value
        value = (value << 4) & 0x3ff0
        data1 = (value >> 8) & 0x3f
        data2 = value & 0xf0
        os.system("i2cset -y {} 0x{:02X} {} {}".format(I2C_BUS, chip_addr, data1, data2))

    def reset(self, opt):
        info = self.opts[opt]
        self.set(opt, info["DEF_VALUE"])

    def get(self, opt):
        return self.read()

    def set(self, opt, value):
        info = self.opts[opt]
        if value > info["MAX_VALUE"]:
            value = info["MAX_VALUE"]
        elif value < info["MIN_VALUE"]:
            value = info["MIN_VALUE"]
        self.write(self.CHIP_I2C_ADDR, value)
