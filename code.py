from utilites import *
#Testing            
colourB = ColourSensor(1)
colourA = ColourSensor(2) #Left sensor
Distance = DistanceSensor(4) #Distance Sensor
#distance = Distanctime.sleep(0.5)eSensor(4) #Distance sensor
motorB = Motor(25,8, 7) #Pass in the GPIO ports - See wiring diagram
motorA = Motor(10,9, 11)
#motorD = Motor(14,15, 18)
#motorC = Motor(13,19, 26)
whiteA = 0.7
blackA = 0.2 
whiteB = 0.7
blackB = 0.2
greenA = 92
greenB = 89
def turnLeft(speed):
    motorA.setSpeed(speed)
    

    #motorC.setSpeed(0.2+speed)
    #motorD.setSpeed(0.2)
    
def turnRight(speed):
    
    motorB.setSpeed(speed)

    #motorC.setSpeed(0.2)
    #motorD.setSpeed(0.2+speed)
    
def leftDetectsBlack():
    if colourB.getVibrance() < whiteB-0.1:
        return True
    else:
        return False
    
def leftOnBlack():
    if colourB.getVibrance() < blackB+0.2:
        return True
    else:
        return False

def rightOnBlack():
    if colourA.getVibrance() < whiteB-0.1:
        return True
    else:
        return False
def rightDetectsBlack():
    if colourA.getVibrance() < blackB+0.2:
        return True
    else:
        return False

def leftDetectsGreen():
    if colourB.getHue() > 90 and colourB.getHue() < 100:
        return True
    else:
        return False

def rightDetectsGreen():
    if colourA.getHue() > 90 and colourA.getHue() < 100:
        return True
    else:
        return False
    
def leftDetectsWhite():
    if colourB.getVibrance() > 0.05:
        return True
    else:
            return False
    
def rightDetectsWhite():
    if colourA.getVibrance() > 0.05:
        return True
    else:
        return False
    
def greenLeft(amountLeft):
    while leftOnBlack() == False:
        motorA.setSpeed(0.1)
        motorB.setSpeed(0.1) 
    while leftDetectsGreen() == False:
        motorB.setSpeed(-0.7)
    while leftDetectsGreen() == True:
        motorA.setSpeed(0.3)
        motorB.setSpeed(0.3)
    
def greenRight(amountRight):
    while rightOnBlack() == False:
        motorA.setSpeed(0.2)
        motorB.setSpeed(0.2) 
    while rightDetectsGreen() == False:
        motorA.setSpeed(-0.7)
    while rightDetectsGreen() == True:
        motorA.setSpeed(0.3)
        motorB.setSpeed(0.3)

def detectsObject():
    if Distance.getDistance() < 50:
        pass
    
    
while True:
    motorA.setSpeed((0.1+whiteA-colourA.getVibrance()))
    motorB.setSpeed((0.1+whiteB-colourB.getVibrance()))
    print(str(colourA.getVibrance()) + " " + str(colourB.getVibrance()))
    #print(colourA.getHue(), colourB.getHue())
    '''if leftDetectsWhite() == True and rightDetectsWhite() == True:
        motorA.setSpeed(0.4)
        motorB.setSpeed(0.4)
        
    if leftDetectsGreen() == True and rightDetectsGreen() == True:
        motorA.setSpeed(0.5)
        motorB.setSpeed(-0.5)
        time.sleep(1)

    if leftDetectsGreen() == True:
        greenLeft(0.5)
        print('greenleft')
    
    if rightDetectsGreen() == True:
        greenRight(0.5)
        print('greenright')

    if leftDetectsBlack() == True:
        motorA.setSpeed(0.5)
        motorB.setSpeed(0.3)
    elif leftOnBlack() == True:
        turnLeft(0.7)
        
    if rightDetectsBlack() == True:
        motorB.setSpeed(0.5)
        motorA.setSpeed(0.3)
    elif rightOnBlack == True:
        turnRight(0.7)'''
