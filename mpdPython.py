#! /usr/bin/python
import subprocess
import serial
import json
from pprint import pprint
from threading import Timer
import time
from mpd import MPDClient
client = MPDClient()
client.timeout = 10
client.idletimeout = None
client.repeat = 1
previous = ''
data = ''
#IP = 'localhost'
IP = 'NucYou'
port = 6600
playPause = True

def launchMopidy():
    process = subprocess.Popen(["mopidy"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            if 'MPD server running' in output:
                print ">" + output.strip()
                return "go"
    return "nogo"
    

def connect():
    try:
        client.connect(IP, port)
        print "mopidy connected"
    except :
	print 'error'

def timeout():
    global previous
    print('timeout : ' + previous)
    previous = ' '
    
def launch(name):
    print(name)
    try:
        client.update()
        client.clear()
        client.load(name)
        playPause = True
        play()
    except:
        connect()
        launch(name)

def nex():
    try:
        client.next()
    except:
        connect()
        next()

def prev():
    try:
        client.previous()
    except:
        connect()
        prev()

def playpause():
    if playPause == True:
        pause()
    else:
        play()

def play():
    global playPause
    playPause = True
    try:
        client.play()
    except:
        connect()
        play()

def pause():
    global playPause
    playPause = False
    try:
        client.pause()
    except:
        pause()

def findPlaylist(playlist):
    global data
    for tags in data:
        for tag in tags:
            if tag == playlist:
                return tags[tag]
    return 'none'

if __name__ == '__main__':
    #time.sleep(60)
    if launchMopidy() == "go":
        print "mopidy launched"
    connect()
    with open('tags.json') as file:
        data = json.load(file)
    locations=['/dev/ttyUSB0','/dev/ttyUSB1', '/dev/cu.usbmodem14221' , '/dev/cu.usbmodem1411', '/dev/ttyACM0','/dev/ttyACM1']
    while True:
        for device in locations:
            try:
                print "Trying...",device
                arduino = serial.Serial(device, 9600)
                break
            except:
                print('Failed to connect to device')
        print('connected')
    
        while True:
            id = arduino.readline().strip()
            print(id)
            if id != previous:
                print id
                previous = id
                playlist = findPlaylist(id)
                if playlist != 'none':
                    launch(playlist)
                else:
                    if id == '560010571706':
                        nex()
                    if id == '560010573021':
                        prev()
                    if id == '560010571C0D' or id == '560010571100':
                        playpause()
            t = Timer(1, timeout)
            t.start()
    arduino.close()
