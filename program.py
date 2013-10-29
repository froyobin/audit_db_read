#!/usr/bin/python
from __future__ import division
import random
import os
import time
from subprocess import Popen,PIPE
for i in range(1,10):
#    print random.randint(10,20)
    pass


def dead_loop_1():
    i = random.randint(1,3)
    while True:
        print "a"
        time.sleep(i)

def dead_loop_10():
    i = random.randint(1,100)
    while True:
        print "b"
        time.sleep(i/10)
def dead_loop_100():
    i = random.randint(1,100)
    while True:
        print "c"
        time.sleep(i/100)
def dead_loop_1000():
    i = random.randint(1,100)
    while True:
        print "d"
        time.sleep(i/1000)
def dead_loop():
    while True:
        print "abcd"
def my_start_dead_loop():
    child_pid = os.fork()
    if child_pid ==0:
        choose = random.randint(1,5)
        print "time we choose to run %d"%choose
        
        case_dic = {1:lambda :dead_loop_1(),\
                    2:lambda :dead_loop_10(),\
                    3:lambda :dead_loop_100(),\
                    4:lambda :dead_loop_1000(),\
                    5:lambda :dead_loop()}

        case_dic[choose]()
    else:
        print child_pid
        sleeptime = random.randint(1,300)
        print "we will sleep %d"%sleeptime
        time.sleep(sleeptime)
        cents = "kill -9 %d" % child_pid
        os.system(cents)
        print "killed"
        os.wait()
        print "finish one"

        print "father: PID %s"%os.getpid()
def heavy_work():
    print "heavy work"
    p1 = Popen(["echo","scale=900000;4*a(1)"], stdout=PIPE)
    p2 = Popen(["bc", "-l"], stdin=p1.stdout)
    p1.stdout.close()
    p1.kill()
    time.sleep(random.randint(1,300))
    p2.kill()
    p1.wait()
    print "heavy work finish"



if __name__ =='__main__':
    child_pid = os.fork()
    if child_pid == 0:
        while True:
            
            my_start_dead_loop()
            time.sleep(random.randint(1,600))
    else:
        while True:
            timeme = random.randint(1,2000)
            print "heavy work sleep %d"% timeme
            time.sleep(timeme)
            heavy_work()

