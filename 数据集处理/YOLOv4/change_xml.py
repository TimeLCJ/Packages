import os
import xml.etree.ElementTree as ET

"""
Modify the content of the 'filename' field, and modify 'name' in all 'object' to 'oboat'
"""

path = './label'
result = './label_new'
class_name = 'oboat'
if not os.path.exists(result):
    os.mkdir(result)

files = os.listdir(path)
for i, file in enumerate(files):
    in_file = os.path.join(path, file)
    with open(in_file) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        fn = root.find('filename').text
        root.find('filename').text = 'other_boat_'+fn[:-5]+'.jpg'
        for obj in root.iter('object'):
            obj.find('name').text = class_name
        r = ET.ElementTree(root)
        r.write(os.path.join(result, file), xml_declaration=False, encoding='utf-8')