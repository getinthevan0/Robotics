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
    def getVibrance(self):
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
#colourB = ColourSensor(2) #Left sensor
#colourC = ColourSensor(3) #Front sensor
#distance = DistanceSensor(4) #Distance sensor
while True: 
    print(colourA.getHue())

    if colourA.getVibrance() < 0.01:
        # If right sensor touches black turn right 15 degrees
         pass
    if colourB.getVibrance() < 0.01:
        # If left sensor touches black turn left 15 degrees
         pass
     if colourA.getHue() > 100 and colourA.getHue() < 140:
        #Move the right at 30 degrees until right sensor touches black
         pass
    if colourB.getHue() > 100 and colourB.getHue() < 140:
        #Move to the left at 30 degrees until left sensor touches black
         pass
    if distance.getDistance() < 100:
        #Turn 90 degrees right
        #Move at 30 degrees left for _ seconds
        #When right sensor touches black, turn right until it is no longer touching black
         pass
     if colourA.getSaturation() > 2:
        #Turn right 45 degrees
        #move left slowly
         pass
#Black = 70, White = 79, Green = 92
    
