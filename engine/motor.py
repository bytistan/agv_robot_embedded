import Jetson.GPIO as GPIO

class Motor:
    def __init__(self, in1_pin, in2_pin, en_pin, frequency=1000):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.en_pin = en_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.en_pin, frequency)
        self.pwm.start(0)

    def forward(self, speed):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def backward(self, speed):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
