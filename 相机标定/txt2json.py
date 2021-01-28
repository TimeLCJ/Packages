import os
import json
import numpy as np

# camera_size = "720"
# txt_para_path = './calibrate_img/divided_'+camera_size+'/para'
txt_para_path = './para'
json_para_result = './'
size = [1280, 960]

if not os.path.exists(json_para_result):
    os.makedirs(json_para_result)

left_camera_matrix = []
right_camera_matrix = []
left_distortion = []
right_distortion = []
R = []
T = []

with open(os.path.join(txt_para_path, 'lim.txt'), 'r') as f:
    for i in f.readlines():
        left_camera_matrix.append([float(j) for j in i.split('\t') if j!=''])
with open(os.path.join(txt_para_path, 'lrd.txt'), 'r') as rd:
    with open(os.path.join(txt_para_path, 'ltd.txt'), 'r') as td:
        rd = [float(j) for j in rd.readline().split('\t') if j != '']
        left_distortion.append(rd[:2])
        td = [float(j) for j in td.readline().split('\t') if j != '']
        left_distortion.append(td)
        if len(rd) > 2:
            left_distortion.append(rd[2:])
        else:
            left_distortion.append([0.0])

with open(os.path.join(txt_para_path, 'rim.txt'), 'r') as f:
    for i in f.readlines():
        right_camera_matrix.append([float(j) for j in i.split('\t') if j!=''])
with open(os.path.join(txt_para_path, 'rrd.txt'), 'r') as rd:
    with open(os.path.join(txt_para_path, 'rtd.txt'), 'r') as td:
        rd = [float(j) for j in rd.readline().split('\t') if j != '']
        right_distortion.append(rd[:2])
        td = [float(j) for j in td.readline().split('\t') if j != '']
        right_distortion.append(td)
        if len(rd) > 2:
            right_distortion.append(rd[2:])
        else:
            right_distortion.append([0.0])

with open(os.path.join(txt_para_path, 'rotation.txt'), 'r') as f:
    for i in f.readlines():
        R.append([float(j) for j in i.split('\t') if j!=''])
with open(os.path.join(txt_para_path, 'translation.txt'), 'r') as f:
    T = [float(j) for j in f.readline().split('\t') if j != '']

left_camera_matrix = np.array(left_camera_matrix).T
left_distortion = np.array([j for i in left_distortion for j in i]).reshape(1, -1)
right_camera_matrix = np.array(right_camera_matrix).T
right_distortion = np.array([j for i in right_distortion for j in i]).reshape(1, -1)
R = np.array(R).T
T = np.array(T).reshape(-1, 1)

dic = {}
dic["size"]=size
dic["left_camera_matrix"] = left_camera_matrix.tolist()
dic["left_distortion"] = left_distortion.tolist()
dic["right_camera_matrix"] = right_camera_matrix.tolist()
dic["right_distortion"] = right_distortion.tolist()
dic["R"] = R.tolist()
dic["T"] = T.tolist()

file = open(os.path.join(json_para_result,
                         os.path.dirname(__file__).split('/')[-1] + '_' + str(size[1]) + ".json"), "w")
json.dump(dic, file)
print("parameter saved in para_"+str(size[1])+".json!")
