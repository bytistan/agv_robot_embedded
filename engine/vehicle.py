import Jetson.GPIO as GPIO

class Vehicle:
    def __init__(self):
        self.motor_nw = MotorController(in1_pin=24, in2_pin=23, en_pin=12)
        self.motor_sw = MotorController(in1_pin=11, in2_pin=25, en_pin=13)
        self.motor_se = MotorController(in1_pin=17, in2_pin=27, en_pin=18)
        self.motor_ne = MotorController(in1_pin=22, in2_pin=5, en_pin=19)

    def forward(self, speed):
        self.motor_nw.forward(speed)
        self.motor_sw.forward(speed)
        self.motor_se.forward(speed)
        self.motor_ne.forward(speed)

    def backward(self, speed):
        self.motor_nw.backward(speed)
        self.motor_sw.backward(speed)
        self.motor_se.backward(speed)
        self.motor_ne.backward(speed)

    def right(self, speed):
        self.motor_nw.backward(speed)
        self.motor_ne.forward(speed)
        self.motor_sw.forward(speed)
        self.motor_se.backward(speed)

    def left(self, speed):
        self.motor_nw.forward(speed)
        self.motor_ne.backward(speed)
        self.motor_sw.backward(speed)
        self.motor_se.forward(speed)

    def turning_right(self, speed):
        self.motor_nw.forward(speed)
        self.motor_ne.backward(speed)
        self.motor_sw.forward(speed)
        self.motor_se.backward(speed)

    def turning_left(self, speed):
        self.motor_nw.backward(speed)
        self.motor_ne.forward(speed)
        self.motor_sw.backward(speed)
        self.motor_se.forward(speed)

    def stop(self):
        self.motor_nw.stop()
        self.motor_sw.stop()
        self.motor_se.stop()
        self.motor_ne.stop()

    def cleanup(self):
        self.motor_nw.cleanup()
        self.motor_sw.cleanup()
        self.motor_se.cleanup()
        self.motor_ne.cleanup()

    def update(self,order,speed):
        if order == 0:
            pass            
