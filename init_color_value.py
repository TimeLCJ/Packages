import cv2

img_path = '100.jpg'
# red = (528, 339)
# yellow = (185, 318)
# blue = (501, 315)
red = (359, 195)
brown = (246, 206)
blue = (360, 201)
img = cv2.imread(img_path)

red_v = img[red[1], red[0]]
brown_v = img[brown[1], brown[0]]
blue_v = img[blue[1], blue[0]]

print(f'red {red_v}')
print(f'brown {brown_v}')
print(f'blue {blue_v}')