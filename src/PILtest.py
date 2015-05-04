# -*- coding: cp936 -*-  

from PIL import Image
from PIL import Image

import win32ui
#test = Image.open("c:\\aaa\\C000201.jpg")
#test.save("c:\\aaa\\temp.png")

im = Image.open("c:\\aaa\\temp.png")

# PIL complains if you don't load explicitly
im.load()

# Get the alpha band
alpha = im.split()[-1]

im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

# Set all pixel values below 128 to 255,
# and the rest to 0
mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)

# Paste the color of index 255 and use alpha as a mask
im.paste(255, mask)

# The transparency index is 255
im.save("c:\\aaa\\logo_py.png", transparency=255)
print("OK")


