
import re
import PIL
from glob import glob
from PIL import Image, ImageEnhance, ImageOps


(PATH_IN, PATH_OUT) = ('./Notebooks/Volume04/', './out/')
(width, height) = (1680, 1200)

page = 'Scan 2.jpeg'
files = glob(PATH_IN+'Scan *')
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
    im = im.resize((width, height))
    im.save(PATH_OUT+str(i).zfill(len(numFiles)+1)+'.jpg', 'JPEG')
