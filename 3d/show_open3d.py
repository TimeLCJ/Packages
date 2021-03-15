import os
import pandas as pd
import open3d as o3d
import numpy as np

basedir = './examples/withboat_concate_results/'
csv_file = "20200929-164618.jpg_0"
csv_file_total = csv_file+'_total.csv'
csv_file_boat = csv_file+'_boat.csv'


csv_path_total = os.path.join(basedir, csv_file_total)
csv_path_boat = os.path.join(basedir, csv_file_boat)


with open(csv_path_total)as f:
    data_total = pd.read_csv(f)
with open(csv_path_boat) as f:
    data_boat = pd.read_csv(f)

# points_total = data_total.values
# points_total = np.asarray(points_total)
# # test
# points_total = points_total[points_total[:, 1] > -5000]
# points_total = points_total[points_total[:, 1] < 2000]
#
# xyz = points_total[:, :3]
#
# bgr = points_total[:, 3:] / 255
# rgb = bgr[..., [2, 1, 0]]
#
# total = o3d.geometry.PointCloud()
# total.points = o3d.utility.Vector3dVector(xyz)
# total.colors = o3d.utility.Vector3dVector(rgb)
# o3d.visualization.draw_geometries([total])

points_boat = data_boat.values
points_boat = np.asarray(points_boat)

# if len(points_boat) != 0:
#     min_z = np.min(points_boat[:, 2])
#     points_boat = points_boat[points_boat[:, 2] < min_z+5000]
xyz = points_boat[:, :3]
bgr = points_boat[:, 3:] / 255
rgb = bgr[..., [2, 1, 0]]

boat = o3d.geometry.PointCloud()
boat.points = o3d.utility.Vector3dVector(xyz)
boat.colors = o3d.utility.Vector3dVector(rgb)
o3d.visualization.draw_geometries([boat])
