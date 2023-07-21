import gpiozero
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_VL53L1X import PiicoDev_VL53L1X
from PiicoDev_Buzzer import PiicoDev_Buzzer
from PiicoDev_Servo import PiicoDev_Servo, PiicoDev_Servo_Driver
import time

#Class for interacting with colour sensors
class ColourSensor:
    def __init__(self, bus):
        if bus < 1 or bus > 4:
            raise ValueError('Bus must be between 1 and 4 (1, 2, 3 or 4)')
        self.sensor = PiicoDev_VEML6040(bus=bus)
        
    #Get the hue of the reflected colour - useful for determining colour such as green, red, blue
    def getHue(self):
        return self.sensor.readHSV()['hue']
    
    #Get the saturation of the reflected colour - useful for determining shade such as white, black
    def getSaturation(self):
        return self.sensor.readHSV()['sat']
    
    #Get the vibrance of the reflected colour - useful for determining reflectiveness ie silver, not silver
    def getValue(self):
        return self.sensor.readHSV()['val']
    
    #Get the combined hue saturation and vibrance of the reflected colour, get with hsv['hue'], hsv['saturation'] and hsv['vibrance']
    def getHSV(self):
        return self.sensor.readHSV()
    
    #Get the name of the colour 'cyan', 'green', 'blue' - Less reliable
    def getColour(self):
        return self.sensor.classifyHue()

#Class for interacting with distance sensors
class DistanceSensor:
    def __init__(self, bus):
        if bus < 1 or bus > 4:
            raise ValueError('Bus must be between 1 and 4 (1, 2, 3 or 4)')
        self.sensor = PiicoDev_VL53L1X(bus=bus)
        
    #Get distance in mm
    def getDistance(self):
        return self.sensor.read()
    
    #Get distance in mm
    def getDistance_mm(self):
        return self.sensor.read()
    
    #Get distance in cm
    def getDistance_cm(self):
        return self.sensor.read() / 10.0
    
    #Get distance in metres
    def getDistance_m(self):
        return self.sensor.read() / 1000.0
    
#Class for interacting with buzzer
class Buzzer:
    def __init__(self, bus, volume=2):
        if bus < 1 or bus > 4:
            raise ValueError('Bus must be between 1 and 4 (1, 2, 3 or 4)')
        self.buzzer = PiicoDev_Buzzer(bus=bus, volume=volume)

    #Get the frequency of a note from the name   
    def getNoteFrequency(note):
        notes = {'C4':262,
                      'C':262,
                      'C#':277,
                      'Db':277,
                      'D':294,
                      'D#':311,
                      'Eb':311,
                      'E':330,
                      'F':349,
                      'F#':370,
                      'Gb':370,
                      'G':392,
                      'G#':415,
                      'Ab':415,
                      'A':440,
                      'A#':466,
                      'Bb':466,
                      'B':494,
                      'C^':523,
                      'C5':523,
                      'rest':0,
                      '':0,
                        }
        note = note.upper()
        if note in notes:
            return notes[note]
        else:
            return 0
        
    #Play a tone without waiting - frequency: the hz of the note - duration: time of note in milleseconds 
    def beginTone(self, frequency=262, duration=500):
        self.buzzer.tone(frequency, duration)
        
    #Play a tone without waiting - frequency: the name of the note - duration: time of note in milleseconds 
    def beginNote(self, note, duration=500):
        self.buzzer.tone(Buzzer.getNoteFrequency(note), duration)

    #Play a tone while waiting - frequency: the hz of the note - duration: time of note in milleseconds 
    def tone(self, frequency=262, duration=500):
        self.buzzer.tone(frequency, duration)
        time.sleep(duration * 0.001)
        
    #Play a tone while waiting - frequency: the name of the note - duration: time of note in milleseconds 
    def play(self, note, duration=500):
        self.buzzer.tone(Buzzer.getNoteFrequency(note), duration)
        time.sleep(duration * 0.001)

    #Play a collection of notes and durations
    def playMelody(self, melody):
        for x in melody:
            self.play(x[0], x[1])
            time.sleep(x[1] * 0.001)

#Class for interacting with servos
class Servo:
    def __init__(self, driver, channel): #There is no need to call this function use ServoDriver.getServo instead
        if channel < 1 or channel > 2:
            raise ValueError('Channel must be 1 or 2')
        self.servo = PiicoDev_Servo(driver.controller, channel)

    #Get the servos angle in degrees
    def getAngle(self):
        return self.servo.angle

    #Set the angle of the servo in degrees
    def setAngle(self, angle):
        self.servo.angle = angle
        
    #Turn the servo a specified number of degrees, a negative turn angle turns left, a positive turn angle turns right
    def turn(self, angle):
        if (self.servo.angle + angle) < 0 or (self.servo.angle + angle) > 180:
            raise ValueError('Turn angle too large!')
        self.servo.angle = self.servo.angle + angle

#Class for getting servos
class ServoDriver:
    def __init__(self, bus):
        if bus < 1 or bus > 4:
            raise ValueError('Bus must be between 1 and 4 (1, 2, 3 or 4)')
        self.controller = PiicoDev_Servo_Driver(bus=bus)

    #Get servo 
    def getServo(self, channel):
        if channel < 1 or channel > 2:
            raise ValueError('Channel must be 1 or 2')
        return Servo(self, channel)

#Class for getting motors
class Motor:
    def __init__(self, forward, backward, pwm):
        self.forward = gpiozero.OutputDevice(forward)
        self.backward = gpiozero.OutputDevice(backward)
        self.pwm = gpiozero.PWMOutputDevice(pwm)

        self.forward.off()
        self.backward.off()
        self.pwm.value = 0

    #Set speed to 0 and wait for 100ms for the action to be completed
    def stop(self):
        self.forward.off()
        self.backward.off()
        self.pwm.value = 0
        time.sleep(0.1)

    #Get speed of motor betwen -1.0 (backwards) and 1.0 (forwards), 0.0 means the motor is stopped
    def getSpeed(self):
        if self.forward.is_lit:
            return self.pwm.value
        elif self.backward.is_lit:
            return -self.pwm.value
        else:
            return 0
        
    #Set the speed of the motor betwen -1.0 (backwards) and 1.0 (forwards), 0.0 stops the motor
    def setSpeed(self, speed):
        if speed == 0:
            self.forward.off()
            self.backward.off()
            self.pwm.value = 0
        elif speed > 0:
            self.forward.on()
            self.backward.off()
            self.pwm.value = speed
        else:
            self.forward.off()
            self.backward.on()
            self.pwm.value = -speed
            
            
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