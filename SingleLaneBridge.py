import threading
import sys
import random

#Creating shared data class
class shared_data:
    time = 1
    redCWaiting = 0
    blueCWaiting = 0
    redCCrossed = 1
    blueCCrossed = 1
    bridgeLock = threading.Lock()
    bridgeCond = threading.Condition(bridgeLock)

    def arrival(self):
        self.bridgeLock.acquire()
        #Name of the thread currently running
        myname = threading.currentThread().getName()
        if(myname == "Red"):
            print("A " + myname + " car arrived at Time" + str(self.time) + "\n")
            self.redCWaiting = self.redCWaiting + 1
        else:
            print("\t\t\t\t\t\tA " + myname + " car arrived at Time" + str(self.time) + "\n")
            self.blueCWaiting = self.blueCWaiting + 1
        self.time = self.time + 1
        #Releasing lock
        self.bridgeLock.release()

    def crossing(self):
        #Crossing the bridge
        self.bridgeLock.acquire()
        try:
            myname = threading.currentThread().getName()
            if(myname == "Red"):
                while not(self.blueCWaiting == 0 or (self.redCCrossed/self.blueCCrossed) <= 1):
                    self.bridgeCond.wait()
                print("A " + myname + " car passing at Time" + str(self.time) + "\n")
                self.time = self.time + 1
                print("\t\t\t\t\t\tA " + myname + " car passed at Time" + str(self.time) + "\n")
                self.time = self.time + 1
                self.redCWaiting = self.redCWaiting - 1
                self.redCCrossed = self.redCCrossed + 1
                self.bridgeCond.notify_all()
            else:
                while not(self.redCWaiting == 0 or (self.blueCCrossed/self.redCCrossed) <= 1):
                    self.bridgeCond.wait()
                print("\t\t\t\t\t\tA " + myname + " car passing at Time" + str(self.time) + "\n")
                self.time = self.time + 1
                print("A " + myname + " car passed at Time" + str(self.time) + "\n")
                self.time = self.time + 1
                self.blueCWaiting = self.blueCWaiting - 1
                self.blueCCrossed = self.blueCCrossed + 1
                self.bridgeCond.notify_all()
        finally:
            self.bridgeLock.release()

#The function every thread executes
def worker(data):

    data.arrival()
    data.crossing()

def main():

    #Using -h and --help arguments
    if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print(" Usage: python SingleLaneBridge.py [Number Of Cars]\n In case the number of cars is not specified, the script will run for N=5")
        sys.exit(0)

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 5
    data = shared_data()
    print("Left Side\t\t\tBridge\t\t\t Right Side\n")

    #0-> We create a new red car, 1-> We create a blue car
    for i in range(0,n):
        x = random.randint(0,1)
        if(x==0):
            t = threading.Thread(name="Red",target=worker, args=(data,))
            t.start()
        else:
            t = threading.Thread(name="Blue",target=worker, args=(data,))
            t.start()

if __name__ == '__main__':
    main()
