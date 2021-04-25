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
