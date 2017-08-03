# Imports
import webiopi
import time
import os, sys #mkdir(path)
import random

GPIO = webiopi.GPIO
webiopi.setDebug()

TRANS_PIN_BCM_NO = 23
moduleIdList = []

usleep = lambda x: time.sleep(x/1000000.0)

# Called by WebIOPi at script loading
def setup():
    GPIO.setFunction(TRANS_PIN_BCM_NO, GPIO.OUT)
    try:
        webiopi.debug("RemotePi Started")


    except Exception as Err:
        webiopi.debug('%s' % Err)

# Looped by WebIOPi
#def loop():
#    webiopi.sleep(1)        
 
# Called by WebIOPi at server shutdown
def destroy():
    try:
        webiopi.debug("Script with macros - Destroy")

    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def addSwitch():
    moduleId = 0

    while True:
        moduleId = random.randrange(100000, 999999)
        if not moduleId in moduleIdList:
            moduleIdList.append(moduleId)
            break
    webiopi.debug ('moduleId : [%s]' % moduleId )

    sendData(moduleId, 9, retry = 5)
    webiopi.debug ('moduleIdList : [%s]' % moduleIdList )

@webiopi.macro
def pairingSwitch():
    addSwitch()

@webiopi.macro
def switchOnModuleId(moduleId):
    sendData(moduleId, 9)

@webiopi.macro
def switchOffModuleId(moduleId):
    sendData(moduleId, 1)

@webiopi.macro
def switchOnModuleIndex(mIndex):
    moduleIndex = int(mIndex)
    if moduleIndex < len(moduleIdList):
        switchOnModuleId(moduleIdList[0])

@webiopi.macro
def switchOffModuleIndex(mIndex):
    moduleIndex = int(mIndex)
    if moduleIndex < len(moduleIdList):
        switchOffModuleId(moduleIdList[0])

def sendData(moduleId, data, retry = 3):
    try:
        for n in range(0, retry):
            rtc = rfsendData(moduleId, data)
            webiopi.debug ('[%d] SendData : %s' % (n, rtc))
            time.sleep(1)

    except Exception as err:
        webiopi.debug ('%s' % err)

def rfsendData(moduleId, data):
    stringData = int('%d%d' % (moduleId, data))
    binData = "{0:b}".format(stringData)

    for a in range(0, 10):
        #print ('binData : [%d]->[%s]' % (stringData, binData))
        for bit in binData:
            if int(bit):
                #print ('high')
                transmit(3, 1)
            else:
                #print ('low')
                transmit(1, 3)
        transmit(1,31)

    return binData

def transmit(nHighPulses, nLowPulses):
    GPIO.digitalWrite(TRANS_PIN_BCM_NO, True)
    usleep(350*nHighPulses)
    GPIO.digitalWrite(TRANS_PIN_BCM_NO, False)
    usleep(350*nLowPulses)
