import picamera
import time
import RPi.GPIO as GPIO
import os

from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/pi/makeuoft/MakeUofT-e3c98ff21819.json'
client = vision.ImageAnnotatorClient()

# GPIO.setmode(GPIO.BOARD)

# # set up GPIO pins
# GPIO.setup(7, GPIO.OUT) # Connected to PWMA
# GPIO.setup(11, GPIO.OUT) # Connected to AIN2
# GPIO.setup(12, GPIO.OUT) # Connected to AIN1
# GPIO.setup(13, GPIO.OUT) # Connected to STBY

recyclable = ["paper", "can", "bottle", "cardboard", "carton", "boxes"]
compostable = ["vegetable", "fruit", "plant", "natural foods", "produce"]

trashCount = [0, 0]
def sortTrash(trashLabel):
    print(trashLabel.description)
    if (trashLabel.score > 0.8):
        for r in recyclable:
            if (r in trashLabel.description.lower()):
                trashCount[1] += 1
                return
        for c in compostable:
            if (c in trashLabel.description.lower()):
                trashCount[0] += 1

def outcome():
    if (trashCount[0] > 0):
        print("put it in compost!")
    elif (trashCount[1] > 0):
        print("put it in recycling")
    else:
        print("put it in garbage")

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('trash.jpg')

def main():
    takephoto()
    """Run a label request on a single image"""

    with open('trash.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)

    response = client.label_detection(image=image)
    data = response.label_annotations

    for d in data:
        sortTrash(d)

    outcome()

        #     # Drive the motor clockwise
        #     GPIO.output(12, GPIO.HIGH) # Set AIN1
        #     GPIO.output(11, GPIO.LOW) # Set AIN2

        #     # Set the motor speed
        #     GPIO.output(7, GPIO.HIGH) # Set PWMA

        #     # Disable STBY (standby)
        #     GPIO.output(13, GPIO.HIGH)

        #     # Wait 5 seconds
        #     time.sleep(5)
    

if __name__ == '__main__':
    main()
