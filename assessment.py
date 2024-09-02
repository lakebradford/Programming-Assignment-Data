from lxml import etree
from PIL import Image, ImageDraw
import json
import os


class screenHierarchy:
    def __init__(self):
        self.fileNames = None
        self.invalidFileNames = []

    def getAnnotatedImages(self):
        rawInput  = input("Enter file names ")
        self.fileNames = set(rawInput.split())
        self.getAnnotatedImages()
        folder = "annotated_images"
        os.makedirs(folder, exist_ok=True)
        for file in self.fileNames:
            try: 
                tree = etree.parse(file+".xml")
                root = tree.getroot()
                srcImg = Image.open(file+".png")
                for child in root.iter("*"):
                    if len(child) == 0:
                        bounds = child.get("bounds")
                        self.drawSquare(bounds, srcImg)
                srcImg.save(os.path.join(folder, file + ".annotated.png"), "png")
            except:
                self.invalidFileNames.append(file)

        if len(self.invalidFileNames) > 0:
            print("The following files are invalid ", self.invalidFileNames)

    def drawSquare(self, bounds, srcImg):
        draw = ImageDraw.Draw(srcImg)
        coords = json.loads(bounds.replace("][", ","))
        draw.rectangle(coords, outline="yellow", width=10)

files = {"com.apalon.ringtones","com.dropbox.android","com.giphy.messenger-1","com.giphy.messenger-2","com.google.android.apps.transalte","com.pandora.android", "com.yelp.android"}
hierarchy = screenHierarchy()

hierarchy.convertFileNames()

        