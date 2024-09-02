from lxml import etree
from PIL import Image, ImageDraw
import json
import os


def getAnnotatedImages():
    rawInput  = input("Enter file names: ")
    fileNames = set(rawInput.split())
    invalidFileNames = []
    validFileNames = []
    folder = "annotated_images"
    os.makedirs(folder, exist_ok=True)
    for file in fileNames:
        try: 
            tree = etree.parse(file+".xml")
            root = tree.getroot()
            srcImg = Image.open(file+".png")
            for child in root.iter("*"):
                if len(child) == 0:
                    bounds = child.get("bounds")
                    drawSquare(bounds, srcImg)
            validFileNames.append(file)
            srcImg.save(os.path.join(folder, file + ".annotated.png"), "png")
        except:
            invalidFileNames.append(file)

    if len(invalidFileNames) > 0:
        print("The following files are invalid: ", invalidFileNames)
    if len(validFileNames) > 0:
        print("Successfully annotated the following files: ", validFileNames)

def drawSquare(bounds, srcImg):
    draw = ImageDraw.Draw(srcImg)
    coords = json.loads(bounds.replace("][", ","))
    draw.rectangle(coords, outline="yellow", width=10)


getAnnotatedImages()