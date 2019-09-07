import RPi.GPIO as gpio
from time import sleep


class actu:

    def __init__(self, pin_esc, pin_servo_1, pin_servo_2, initial_freq):

        self.pin_esc = pin_esc
        self.pin_servo_1 = pin_servo_1
        self.pin_servo_2 = pin_servo_2

        # need experiment
        self.constup_value = 0
        self.constay_value = 0
        self.breakon_value = 0
        self.breakoff_value = 0
        self.tune_const_speed = 0
        self.tune_initial_duty = 0
        self.tune_const_duty = 0

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        
        gpio.setup(self.pin_esc, gpio.OUT)
        gpio.setup(self.pin_servo_1, gpio.OUT)
        gpio.setup(self.pin_esc, gpio.OUT)

        self.esc = gpio.PWM(self.pin_esc, initial_freq)
        self.ser_1 = gpio.PWM(self.pin_servo_1, initial_freq)
        self.ser_2 = gpio.PWM(self.pin_servo_2, initial_freq)
        sleep(0.5)

        self.esc.start(0)
        self.ser_1.start(self.breakon_value)
        self.ser_2.start(self.breakon_value)
        sleep(0.5)

        print(">> setup of pwms is done.")

    # esc
    def new_throttle(self, throttle):                                   # change throttle value(0 ~ 100)
        duty = round((throttle + 110.702498) / 19.267136, 2)            # change throttle value to duty
        print(">> change throttle value.")
        self.esc.ChangeDutyCycle(duty)
        print("now duty : %f" % duty)
        print("now throttle value : %d" % throttle)

    def constup(self):
        self.esc.ChangeDutyCycle(self.constup_value)
        print(">> I'm at constant speed!!")

    def constay(self):
        self.esc.ChangeDutyCycle(self.constay_value)
        print(">> I'm ready to fry @^@")

    # servo
    def new_break(self, duty):
        self.ser_1.ChangeDutyCycle(duty)
        self.ser_2.ChangeDutyCycle(duty)
        print(">> change degree of breaks.")

    def breakon(self):
        self.ser_1.ChangeDutyCycle(self.breakon_value)
        self.ser_2.ChangeDutyCycle(self.breakon_value)
        print(">> apply the break.")

    def breakoff(self):
        self.ser_1.ChangeDutyCycle(self.breakoff_value)
        self.ser_2.ChangeDutyCycle(self.breakoff_value)
        print(">> release the break.")

    # tune mode, need to edit
    def tune(self, meter):
        tuning_time = meter / self.tune_const_speed                     # time at constant speed

        print(">> start tuning to go %f meter up." % meter)
        self.esc.ChangeDutyCycle(self.tune_const_duty)
        self.breakoff()
        sleep(tuning_time)

        print(">> the tuning is done. get stopped.")
        self.breakon()
        self.esc.ChangeDutyCycle(0)
        sleep(1)

    def end(self):
        self.esc.stop()
        self.ser_1.stop()
        self.ser_2.stop()
        sleep(0.5)
        gpio.cleanup(self.pin_esc, self.pin_servo_1, self.pin_servo_2)
        sleep(0.5)
        print(">> pwms stopped.")
