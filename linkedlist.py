import threading
from threading import Timer,Thread,Event
from pynput.keyboard import Key, Listener

songListDictionary = {}
counter = 1
songListFile = open("songList.txt","r")
for song in songListFile.readlines():
   songListDictionary[str(counter)] = song
   counter += 1

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
        
        
timerWorking = False
timeElapsed = 0
songupdated = True
previousSong = ""
playList = SLinkedList()
counter = 1
_songTimer= ""
_mainThread= ""

for key,value in songListDictionary.items():
    print(key +" : " + value.strip("\n"))
      
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
                  
    def gotoNext(key):
    global previousSong
    if key.char == 'a':
        try:
            _songTimer.resetTimer()
            previousSong = _songTimer._playList.headval
            _songTimer._playList.headval = _songTimer._playList.headval.nextval
            _songTimer._songupdated = True
        except Exception as e:
            _songTimer.stopTimer()
            print("Play List Ended")
    if key.char == 'b':
        try:
            _songTimer.resetTimer()
            _songTimer._playList.headval = previousSong
            _songTimer._songupdated = True
        except Exception as e:
            _songTimer.stopTimer()
            #print(e)
            print("Reached Start")
    if key.char == 'c':
        try:
            _songTimer.pauseTimer()
            print("Pause")
        except:
            print("error")

    if key.char == 'd':
        try:
            _songTimer.resumeTimer()
            print("Resume")
        except:
            print("error")
    
       
    def Main():
        global previousSong
        while True:
            if(_songTimer._timeElapsed == 5):
                _songTimer.resetTimer()
                previousSong = _songTimer._playList.headval
                _songTimer._playList.headval = _songTimer._playList.headval.nextval
                _songTimer._songupdated = True

    stopFlag = Event()
    _mainThread = threading.Thread(target=Main)
    _songTimer = SongTimer(stopFlag,timerWorking,timeElapsed,playList)
    _songTimer.start()
    _songTimer.startTimer()
    _mainThread.start()
    with Listener(on_release = gotoNext) as listener:   
        listener.join()
