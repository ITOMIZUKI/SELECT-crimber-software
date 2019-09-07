import RPi.GPIO as gpio 
import math
import time
import datetime
import csv

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
        lim_rot = int(goal / (2 * math.pi * diameter) * 1000)    # diameter[mm]
        self.lim_pul = lim_rot * resolution

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin_A, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.pin_B, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.pin_signal, gpio.OUT, initial=gpio.LOW)

        dt = datetime.datetime.now()
        file_name = "encLog_" + str(dt.year) + "." + str(dt.month) + "." + str(dt.day) + "_" + str(dt.hour) + "." + str(dt.minute) + ".csv"
        self.f = open(file_name, "a")
        self.writer = csv.writer(self.f, lineterminator="\n")

        # datasie 2*20000
        self.log = [[0.0, 0]]
        for i in range(19999):
            self.log.append([0.0, 0])

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
        goal_time = 0.0
        num = 0
        sig = 0

        while True:

            self.precount = self.count
            self.deal()

            # main for counting
            now_time = time.time() -initial_time
            if self.precount != self.count:
                #now_time = time.time() - initial_time
                self.log[num] = [now_time, self.count]
                print ("time: %f    count: %d" % (self.log[num][0], self.log[num][1]))
                num += 1

            # write data if no moving for 3 sec and num > 10000
            if (time.time() > now_time + 3) and (num > 300):
                print(">> writing data so far...")
                self.writer.writerows([i for i in self.log if not (i == [0.0, 0])])     # write data except element [0.0, 0]
                print(">> ok, all done.")
                num = 0

            """
            # output signal
            if (sig == 0) and (self.count >= self.lim_pul):
                gpio.output(self.pin_signal, gpio.HIGH)
                sig == 1
                goal_time = now_time

            # stop signal
            if (sig == 1) and (now_time > goal_time + 3.0):
                gpio.output(self.pin_signal, gpio.LOW)
            """
    def end(self):
        self.writer.writerows([i for i in self.log if not (i == [0.0, 0])])
        gpio.cleanup(self.pin_A)
        gpio.cleanup(self.pin_B)
        self.f.close()


if __name__ == "__main__":

    try:
        enc = enco(14, 15, 5, 25, 25, 1)
        enc.go()
        print("check out")
    except KeyboardInterrupt:
        enc.end()
