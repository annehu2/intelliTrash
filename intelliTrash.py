import picamera
import time
import RPi.GPIO as GPIO
import os

from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/pi/makeuoft/MakeUofT-e3c98ff21819.json'
client = vision.ImageAnnotatorClient()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(7, 50)
p1 = GPIO.PWM(13, 50)
p.start(6)
p1.start(7)

recyclable = ["paper", "can", "bottle", "cardboard", "carton", "boxes", "drink"]
compostable = ["vegetable", "fruit", "plant", "natural foods", "produce"]

trashCount = [0, 0]
def sortTrash(trashLabel):
    if (trashLabel.score > 0.8):
        print(trashLabel.description)
        for r in recyclable:
            if (r in trashLabel.description.lower()):
                trashCount[1] += 1
                return
        for c in compostable:
            if (c in trashLabel.description.lower()):
                trashCount[0] += 1

def letsRecycle():
    p.ChangeDutyCycle(2.2)
    time.sleep(2)
    p.ChangeDutyCycle(6)
    time.sleep(1)
    p1.ChangeDutyCycle(3)
    time.sleep(2)
    p1.ChangeDutyCycle(7)
    time.sleep(1)

def letsCompost():
    p.ChangeDutyCycle(2.2)
    time.sleep(2)
    p.ChangeDutyCycle(6)
    time.sleep(1)
    p1.ChangeDutyCycle(11)
    time.sleep(2)
    p1.ChangeDutyCycle(7)
    time.sleep(1)

def letsGarbage():
    p.ChangeDutyCycle(9.8)
    time.sleep(2)
    p.ChangeDutyCycle(6)
    time.sleep(1)

def outcome():
    if (trashCount[0] > 0):
        print("put it in compost!")
        letsCompost()
    elif (trashCount[1] > 0):
        print("put it in recycling")
        letsRecycle()
    else:
        print("put it in garbage")
        letsGarbage()

    p.stop()
    GPIO.cleanup()  

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
    

if __name__ == '__main__':
    main()
