# Libraries
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# The RPi GPIO Pins
TRIG = 18
ECHO = 24
BUZZ = 3

# Set Buzzer, Trig and Echo to OUTPUT mode
GPIO.setup(BUZZ, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Measures the distance between a sensor and and the nearest obstacle
def find_distance():
  GPIO.output(TRIG, True) 
  time.sleep(0.00001) 
  GPIO.output(TRIG, False) 
 
  pulse_start = time.time()
  pulse_stop = time.time()
  
  while GPIO.input(ECHO) == 0:
    pulse_start = time.time()
 
  while GPIO.input(ECHO) == 1:
    pulse_stop = time.time()
  
  measuredTime = pulse_stop - pulse_start
  TotalDistance = measuredTime * 33112 
  ActualDistance = TotalDistance / 2

  print("Distance from nearest object:", ActualDistance, " cm")
  
  # returns measured distance
  return ActualDistance

# Calculates the speed and frequency of beeping depending on the distance
def buzzer_freq():
  
  dist = find_distance()
  
  if dist > 70:
    return -1
  elif dist <= 70 and dist >=50:
    return 1
  elif dist < 50 and dist >= 30:
    return 0.5
  elif dist < 30 and dist >= 20:
    return 0.25
  elif dist < 20 and dist >= 10:
    return 0.10
  else:
    return 0

# Executes all methods / main method
def Execute():
  try:
    while True:
      freq = buzzer_freq()
      
      if freq == -1:
        GPIO.output(BUZZ, False)
        time.sleep(0.25)
      
      elif freq == 0:
        GPIO.output(BUZZ, True)
        time.sleep(0.25)
      
      else:
        GPIO.output(BUZZ, True)
        time.sleep(0.2) 
        GPIO.output(BUZZ, False)
        time.sleep(freq) 
  
  # stops beeping if interupted
  except KeyboardInterrupt:
    GPIO.output(BUZZ, False)
    GPIO.cleanup()

# Since there are many methods in the script it will run Execute() first when the script is run
if __name__ == "__main__":
    Execute()
