import threading
from threading import Timer,Thread,Event

class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None

class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        while printval is not None:
            print(printval.dataval)
            printval = printval.nextval
    
    def AtBegining(self,newData):
        NewNode = Node(newData)
        NewNode.nextval = self.headval
        self.headval = NewNode

    def AtEnd(self,newData):
        NewNode = Node(newData)
        if self.headval is None:
            self.headval = NewNode
            return
        last = self.headval
        while(last.nextval):
            last = last.nextval
        last.nextval = NewNode

    def Inbetween(self,middle_node, newData):
        if middle_node is None:
            print("The mentioned node is absent")
            return
        NewNode = Node(newData)
        NewNode.nextval = middle_node.nextval
        middle_node.nextval = NewNode

class SongTimer(Thread):
    def __init__(self,event,_timerWoking,_timeElapsed,playList):
        self._playList = playList
        self._timerWoking = _timerWoking
        self._timeElapsed = _timeElapsed
        self._songupdated = True
        Thread.__init__(self)
        self.stopped = event

    def startTimer(self):
        self._timerWoking = True
        self._timeElapsed = 0
        
    def pauseTimer(self):
        self._timerWoking = False

    def stopTimer(self):
        self._timeElapsed = 0
        self._timerWoking = False
        self.stopped.set()
    
    def resumeTimer(self):
        self._timerWoking = True

    def resetTimer(self):
        self._timeElapsed = 0

    def run(self):
        while not self.stopped.wait(1):
            if(self._timerWoking==True):
                try:
                    if(self._songupdated):
                        print(("Playing: "+ self._playList.headval.dataval).strip("\n"))
                        self._songupdated = False
                    self._timeElapsed += 1
                except Exception as e:
                    self.stopTimer()
                    print("Play List Ended")