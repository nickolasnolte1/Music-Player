import threading
from threading import Timer,Thread,Event
from pynput.keyboard import Key, Listener
from pynput import keyboard
import os
from classes import SLinkedList, SongTimer


songListDictionary = {}
cicle = True
while cicle:
    option = int (input(""" 
                           WELCOME
                ------ 🎶 Music Player 🎶 ------ 
                1. List of songs 📁
                2. Create playlist and start listening 🔊
                3. Exit ❌

    """))

    if option == 1:
        counter = 1
        songListFile = open("songList.txt","r")
        for song in songListFile.readlines():
            songListDictionary[str(counter)] = song
            counter += 1
        for Key,value in songListDictionary.items():
            print(Key +" : " + value.strip("\n"))
            
    timerWorking = False
    timeElapsed = 0
    songupdated = True
    previousSong = ""
    playList = SLinkedList()
    counter = 1
    _songTimer= ""
    _mainThread= ""

    if option == 2:
        print("")
        print("Press: ")
        print("\tTo play Next Song ⏭️  press: a")
        print("\tTo play Previous Song ⏮️  press: b")
        print("\tTo Pause the Song ⏸️  press: c")
        print("\tTo Resume the Song ⏯️  press: d")
        print("")
        songs = int(input("Please enter how many songs you want to add to your playlist: "))
        for i in range (songs):
            songToPlay = input("Enter Song Number #️⃣ : ")
            playList.AtEnd(songListDictionary[songToPlay])
            
                        
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
                    print("PlayList Ended")
            if key.char == 'b':
                try:
                    _songTimer.resetTimer()
                    _songTimer._playList.headval = previousSong
                    _songTimer._songupdated = True
                except Exception as e:
                    _songTimer.stopTimer()
                    print("Reached Start")
            if key.char == 'c':
                try:
                    _songTimer.pauseTimer()
                    print("Song Paused ⏸️")
                except:
                    print("error")

            if key.char == 'd':
                try:
                    _songTimer.resumeTimer()
                    print("Song Resumed ⏯️")
                except:
                    print("error")
            
        def Main():
            global previousSong
            while True:
                if(_songTimer._timeElapsed == 10):
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

