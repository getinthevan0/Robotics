from utilities import *
# Testing            
colourA = ColourSensor(1) #Right sensor
colourB = ColourSensor(2) #Left sensor
colourC = ColourSensor(3) #Front sensor
distance = DistanceSensor(4) #Distance sensor

# Define the GPIO pins for each motor (replace these with the actual GPIO pins you are using)
MOTOR1_FORWARD_PIN = 17
MOTOR1_BACKWARD_PIN = 18
MOTOR1_PWM_PIN = 22

MOTOR2_FORWARD_PIN = 23
MOTOR2_BACKWARD_PIN = 24
MOTOR2_PWM_PIN = 25

MOTOR3_FORWARD_PIN = 5
MOTOR3_BACKWARD_PIN = 6
MOTOR3_PWM_PIN = 13

MOTOR4_FORWARD_PIN = 19
MOTOR4_BACKWARD_PIN = 26
MOTOR4_PWM_PIN = 12

# Initialize the four motors
motor1 = Motor(MOTOR1_FORWARD_PIN, MOTOR1_BACKWARD_PIN, MOTOR1_PWM_PIN) #front left
motor2 = Motor(MOTOR2_FORWARD_PIN, MOTOR2_BACKWARD_PIN, MOTOR2_PWM_PIN) #front right
motor3 = Motor(MOTOR3_FORWARD_PIN, MOTOR3_BACKWARD_PIN, MOTOR3_PWM_PIN) #back left
motor4 = Motor(MOTOR4_FORWARD_PIN, MOTOR4_BACKWARD_PIN, MOTOR4_PWM_PIN) #back right

def rescue():
        # Turn 90 degrees right
        motor1.setSpeed(0.5);
        motor3.setSpeed(0.5);
        time.sleep(0.2)
        #Move slowly left until the motor detects can
    while True:
        if distance.getDistance() < 100:
            motor1.setspeed(0.1)
            motor2.setspeed(0.1)
            motor3.setspeed(0.1)
            motor4.setspeed(0.1)
            if distance.getDistance() < 50 and colourC.getValue > 0.5:
                # Pick up can
                while True:
                    # Move right slowly until the front color sensor detects orange
                    turnRight(0.1)
                    if colorC.getHue > 20 and colorC.getHue < 40:
                        motor1.setspeed(0.2)
                        motor2.setspeed(0.2)
                        motor3.setspeed(0.2)
                        motor4.setspeed(0.2)
                        if distance.getDistance() < 50:
                            # Put can on platform
        else:
        motor2.setSpeed(0.2)
        motor4.setSpeed(0.2)
        motor1.set(0.1)
        motor3.setSpeed(0.1)
        
def turnRight(speed):
        motor2.setSpeed(0.5);
        motor4.setSpeed(0.5);
        motor1.setSpeed(0.5+speed);
        motor3.setSpeed(0.5+speed);

def turnLeft(speed):        
        motor1.setSpeed(0.5);
        motor3.setSpeed(0.5);
        motor2.setSpeed(0.5+speed);
        motor4.setSpeed(0.5+speed);

    
while True: 
    
    # If right sensor touches black turn right 15 degrees
    if colourA.getHue() > 65 and colourA.getHue() < 75:
        turnRight(0.1)
        
    # If left sensor touches black turn left 15 degrees
    if colourB.getHue() > 65 and colourA.getHue() < 75:
        turnLeft(0.1)   

    
    #If the right sensor touches green, move the right at 30 degrees until right sensor touches black
    if colourA.getHue() > 90 and colourA.getHue() < 100:
        while not(colourB.getHue() > 65 and colourB.getHue() < 75):
            turnRight(0.1)

    
    #If the left sensor touches green, move to the left at 30 degrees until left sensor touches black
    if colourB.getHue() > 90 and colourB.getHue() < 100:
        while not(colourA.getHue() > 65 and colourA.getHue() < 75):
            turnLeft(0.1)

    # If both sensors touch green, turn 180 degrees
    if colourB.getHue() > 90 and colourB.getHue() < 100 and colourA.getHue() > 90 and colourA.getHue() < 100:
        turnRight(0.2)
        
    #If robot detects can, turn 90 degrees right
    if distance.getDistance() < 100:
        turnRight(0.1)
        time.sleep(0.3)
        #Move at 30 degrees left for _ seconds
        turnLeft(0.1)
        #When right sensor touches black, turn right until it is no longer touching black
        if colourB.getHue() > 65 and colourA.getHue() < 75:
            while colourB.getHue() > 65 and colourA.getHue() < 75:
                turnRight()

    # If the left sensor detects silver, perform rescue operation
    if colourA.getSaturation() > 2:
        rescue()
# Hue values for different colours at a distance of ≈ 2cm away: Black = 70, White = 79, Green = 92
    
