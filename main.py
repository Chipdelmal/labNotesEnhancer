
import os
import re
import sys
import PIL
import img2pdf
from glob import glob
from PIL import Image, ImageEnhance

###############################################################################
# This script goes through the files stored in the './notebooks/argv1' folder,
#   processes them to make the scanned images clearer, and stores the output
#   in PDF format.
# -----------------------------------------------------------------------------
#   python main.py SUBFOLDER DeleteFiles FilesPattern
#   python main.py Volume01 OVW Scan
###############################################################################
(PTI, VOL, PTO) = ('./notebooks/', sys.argv[1], './out/')
(OVW, PTRN) = (sys.argv[2], sys.argv[3])
(width, height) = (1680/1, 1200/1)

# Delete existing files in output directory
if OVW == 'OVW':
    delFiles = glob(PTO+'/*')
    for f in delFiles:
        os.remove(f)

# Read filenames in the input directory
files = glob(PTI+VOL+'/'+PTRN+'*')
files.sort(key=lambda f: int(re.sub('\D', '', f)))
numFiles = str(len(files))
fPadNum = len(numFiles)
print('Detected {} files...'.format(numFiles))

# Go through the images in the folder
for (i, page) in enumerate(files):
    print('* Processing ({}/{})'.format(
            str(i+1).zfill(fPadNum), numFiles.zfill(fPadNum)
        ), end='\r')
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
    im.save(PTO+str(i+1).zfill(fPadNum)+'.jpg', 'JPEG')
print('Processed ({}/{})       '.format(
        numFiles.zfill(fPadNum), numFiles.zfill(fPadNum)
    ), end='\n')

# Create PDF from the images
print('Processing PDF...')
files = glob(PTO+'*.jpg')
files.sort(key=lambda f: int(re.sub('\D', '', f)))
with open(VOL+'.pdf', "wb") as f:
    f.write(img2pdf.convert([i for i in files]))

# Delete processed files in output directory
if OVW == 'OVW':
    delFiles = glob(PTO+'/*')
    for f in delFiles:
        os.remove(f)
print('Finished!')
