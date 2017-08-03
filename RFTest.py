import time
import os
import RPi.GPIO as GPIO
usleep = lambda x: time.sleep(x/1000000.0)

class RFPi():
    def __init__(self, mId = 499999, transPinBCM = 23):
        self.TRANS_PIN_BCM_NO = transPinBCM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRANS_PIN_BCM_NO, GPIO.OUT)

        self.setModuleId(mId)
    
    '''
    ModuleId 
    '''
    global moduleId

    def setModuleId(self, mId):
        global moduleId
        moduleId = mId

    def getModuleId(self):
        global moduleId
        return moduleId

    def sendData(self, data):
        stringData = int('%d%d' % (self.getModuleId(), data))
        binData = "{0:b}".format(stringData)

        for a in range(0, 10):
            print ('binData : [%d]->[%s]' % (stringData, binData))
            for bit in binData:
                if int(bit):
                    #print ('high')
                    self.transmit(3, 1)
                else:
                    #print ('low')
                    self.transmit(1, 3)
            self.transmit(1,31)

        return binData


    def transmit(self, nHighPulses, nLowPulses):
        GPIO.output(self.TRANS_PIN_BCM_NO, True)
        usleep(340*nHighPulses)
        GPIO.output(self.TRANS_PIN_BCM_NO, False)
        usleep(340*nLowPulses)

if __name__ == "__main__":
    rfpi = RFPi()
    rfpi.setModuleId(999999)
    while True:
        rfpi.sendData(9)
        time.sleep(1)
        rfpi.sendData(1)
        time.sleep(1)


