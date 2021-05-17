import os

path = './'
imgs = os.listdir(path)

for img in imgs:
    if img[-4:] == '.jpg':
        os.rename(img, '0_'+img)