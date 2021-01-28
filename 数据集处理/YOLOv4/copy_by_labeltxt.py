import os
import shutil

label_path = './test.txt'
img_dir = './img'
result_path = './copied'
if not os.path.exists(result_path):
    os.makedirs(result_path)

f = open(label_path, 'r', encoding='utf-8')
for line in f.readlines():
    data = line.split(" ")
    shutil.copy(os.path.join(img_dir, data[0]), os.path.join(result_path, data[0]))
