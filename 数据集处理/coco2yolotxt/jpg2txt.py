import os

# image_dir = './images/train/'
# img_txt = './train.txt'
image_dir = './total/'
img_txt = './img.txt'

with open(img_txt, 'w') as f:
    for file in os.listdir(image_dir):
        if file[-4:] == '.jpg':
            img_path = image_dir + file
            f.write(img_path+'\n')

