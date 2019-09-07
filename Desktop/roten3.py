import RPi.GPIO as gpio 
import math
import time

class enco:

    def __init__(self, pin_A, pin_B, pin_signal, diameter, resolution, goal):

        self.pin_A = pin_A
        self.pin_B = pin_B
        self.pin_signal = pin_signal
        self.count = 0
        self.precount = 0
        self.sign = 0
        self.lastB = 0
        self.currentB = 0
        lim_rot = int(goal / (2 * math.pi * diameter * 1000))    # diameter[mm]
        self.lim_pul = lim_rot * resolution

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin_A, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.pin_B, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.pin_signal, gpio.OUT, initial=gpio.LOW)

        time.sleep(0.5)
        print(">> setup of encoder is done.")

    def deal(self):
        self.lastB = gpio.input(self.pin_B)

        while not(gpio.input(self.pin_A)):
            self.currentB = gpio.input(self.pin_B)
            self.sign = 1

        if self.sign == 1:
            if self.lastB == 0 and self.currentB == 1:
                self.count += 1
            if self.lastB == 1 and self.currentB == 0:
                self.count -= 1
            self.sign = 0

    def go(self):
        initial_time = time.time()

        while True:
            self.precount = self.count
            self.deal()

            if self.count >= self.lim_pul:
                gpio.output(self.pin_signal, gpio.HIGH)
                time.sleep(2)
                break

            elif self.precount != self.count:
                now_time = time.time() - initial_time
                print("time : %f    count: %d" % (now_time, self.count))

    def end(self):
        gpio.cleanup(self.pin_A, self.pin_B)


if __name__ == "__main__":

    enc = enco(14, 15, 5, 25, 25, 90)
    enc.go()