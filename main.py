
import re
import PIL
import img2pdf
from glob import glob
from PIL import Image, ImageEnhance


(PATH_IN, VOL, PATH_OUT) = ('./notebooks/', 'Volume04', './out/')
(width, height) = (1680/1, 1200/1)

files = glob(PATH_IN+VOL+'/Scan *')
files.sort(key=lambda f: int(re.sub('\D', '', f)))
numFiles = str(len(files))

for (i, page) in enumerate(files):
    im = Image.open(page)
    enhancer = ImageEnhance.Color(im)
    im = enhancer.enhance(.5)
    im = im.rotate(270, PIL.Image.NEAREST, expand=1)
    enhancer = ImageEnhance.Sharpness(im)
    im = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(.85)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.25)
    im = im.resize((int(width), int(height)))
    im.save(PATH_OUT+str(i+1).zfill(len(numFiles)+1)+'.jpg', 'JPEG')


files = glob(PATH_OUT+'*.jpg')
files.sort(key=lambda f: int(re.sub('\D', '', f)))
with open(VOL+'.pdf', "wb") as f:
    f.write(img2pdf.convert([i for i in files]))
