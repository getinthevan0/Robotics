from utilites import * #Import all of the sensors, servo, buzzers and motor classes

colourA = ColourSensor(1) #Get the colour sensor on I2C Bus 1 - See wiring diagram, Colour sensors must be on different busses
colourB = ColourSensor(2) #Get the colour sensor on I2C Bus 2
colourC = ColourSensor(3) #Get the colour sensor on I2C Bus 3
colourD = ColourSensor(3) #Get the colour sensor on I2C Bus 4 - There are a maximum of four colour sensors per group

buzzer = Buzzer(1) #The I2C Bus can be any, of them, just check where you plugged in the buzzer, pass a second value to control volume
#To pass in the volume use Buzzer(I2C_BUS, VOLUME), the default volume is 2(Decibals I believe)

distance = DistanceSensor(1) #Like the Buzzer your distance sensor can be on any I2C bus, just check where it is plugged in

servoDriver = ServoDriver(1) #Get the servo driver, this is needed to get individual servos, but not needed after

servo1 = servoDriver.getServo(1) #Gets the first servo 
servo2 = servoDriver.getServo(2) #Gets the second servo

motorA = Motor(25, 8, 7) #Pass in the GPIO ports - See wiring diagram
motorB = Motor(16, 20, 21) #Pass in the GPIO ports - See wiring diagram
motorC = Motor(13, 19, 26) #Pass in the GPIO ports - See wiring diagram

while True: 
    print(colourA.getHue()) #Get the 'hue' of the colour of colour A, this is best as it is more accurate and more specific, see a HSV colour wheel to interpret the value
    print(colourB.getColour()) #Get the name of the colour, this works but is less accurate, I reccomend using getHue
    print(colourC.getSaturation()) #This will help identify between black and white (possibly silver, but I think getVibrance will work better there)
    print(colourD.getVibrance()) #This will get the vibrance which should help identify silver
    #Alternativly if you want you can use 'colourA.getHSV()' which will return a dictionary of HSV for example "colourA.getHSV()['hue']" will get the hue

    #These buzzer functions DO wait for the sound to finish
    buzzer.tone(262, 500) #Play C4 for 500ms, if left empty like buzzer.tone() it will default to this
    buzzer.play('C4', 500) #Play allows for you to enter a note name instead, the options are all notes 'C', 'D', 'F#', to indicate high C use 'C5', low C is 'C4'
    buzzer.playMelody([['C4', 500], ['D', 500]]) #Play a collection of notes

    #These buzzer functions DONT wait for the sound to finish
    buzzer.beginTone(262, 500) #same as buzzer.tone but doesn't wait
    buzzer.beginNote('C4', 500) #same as buzzer.play but doesn't wait

    print(distance.getDistance()) #Get distance in mm
    print(distance.getDistance_mm()) #Get distance in mm
    print(distance.getDistance_cm()) #Get distance in cm
    print(distance.getDistance_m()) #Get distance in metres

    motorA.stop() #Stop - same as motor.speed(0) with break to wait for stop
    motorB.setSpeed(0.5) #Go forward at half speed
    print(motorB.getSpeed()) #Get the speed of motor B (Expected value is 0.5)
    motorC.setSpeed(-0.75) #Go backward at 75% speed
    print(motorC.getSpeed()) #Get the speed of motor C (Expected value is -0.75)

    servo1.turn(10) #Turn the servo 10 degrees to the right (use negative to turn left)
    servo2.setAngle(45) #Set the angle of the servo to 45 degrees
    print(servo2.getAngle()) #Get the angle of servo 2 (Expected value is 45)
