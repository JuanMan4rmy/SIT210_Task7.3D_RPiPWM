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
 
  start = time.time()
  stop = time.time()
  
  while GPIO.input(ECHO) == 0:
    start = time.time()
 
  while GPIO.input(ECHO) == 1:
    stop = time.time()
  
  measuredTime = stop - start
  distanceBothWays = measuredTime * 33112 
  distance = distanceBothWays / 2

  print("Distance from nearest object:", distance, " cm")
  
  # returns measured distance
  return distance

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
def main():
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

# Since there are many methods in the script it will run main() when the script is run
if __name__ == "__main__":
    main()
