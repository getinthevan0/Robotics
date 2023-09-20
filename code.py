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


def turnLeft(speed):
    motorA.setSpeed(speed)
    motorB.setSpeed(-speed)

    #motorC.setSpeed(0.2+speed)
    #motorD.setSpeed(0.2)
    
def turnRight(speed):
    motorA.setSpeed(-speed)
    motorB.setSpeed(speed)

    #motorC.setSpeed(0.2)
    #motorD.setSpeed(0.2+speed)
    
def leftDetectsBlack():
    if colourB.getVibrance() < 0.025:
        return True
    else:
        return False
    
def leftOnBlack():
    if colourB.getVibrance() < 0.018:
        return True
    else:
        return False

def rightOnBlack():
    if colourA.getVibrance() < 0.018:
        return True
    else:
        return False
def rightDetectsBlack():
    if colourA.getVibrance() < 0.025:
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
    if colourB.getVibrance() > 0.026:
        return True
    else:
        return False
    
def rightDetectsWhite():
    if colourA.getVibrance() > 0.026:
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
    print(colourB.getHSV())
    #print(colourA.getHue(), colourB.getHue())
    if leftDetectsWhite() == True and rightDetectsWhite() == True:
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
        turnLeft(0.4)
        
    elif leftOnBlack() == True:
        turnLeft(0.7)
        
    if rightDetectsBlack() == True:
        turnRight(0.4)
        
    elif rightOnBlack == True:
        turnRight(0.7)
