import os
import pandas as pd
import open3d as o3d
import numpy as np
import cv2

csv_file_boat = '5.7.from.lhq/all_points_with_inf.csv'
img_path = '5.7.from.lhq/fish.jpg'

def pick_points(pcd):
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()

    return vis.get_picked_points()

def custom_draw_geometry_with_custom_fov(pcd, fov_step):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    ctr = vis.get_view_control()
    print("Field of view (before changing) %.2f" % ctr.get_field_of_view())
    ctr.change_field_of_view(step=fov_step)
    print("Field of view (after changing) %.2f" % ctr.get_field_of_view())
    vis.run()
    vis.destroy_window()

#
# with open(csv_path_total)as f:
#     data_total = pd.read_csv(f)
with open(csv_file_boat) as f:
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
if img_path is not None and points_boat.shape[1]<=3:
    bgr = cv2.imread(img_path)
    rgb = bgr[..., [2, 1, 0]] / 255
    rgb = rgb.reshape((-1, 3))
    inds = np.logical_and(points_boat[:, 2]>0, points_boat[:, 2]<10000)
    rgb = rgb[inds]
    xyz = points_boat[inds]
else:
    # moving inf point
    points_boat = points_boat[points_boat[:,2]>0]
    points_boat = points_boat[points_boat[:,2]<10000]

    xyz = points_boat[:, :3]
    bgr = points_boat[:, 3:] / 255
    rgb = bgr[..., [2, 1, 0]]

boat = o3d.geometry.PointCloud()
boat.points = o3d.utility.Vector3dVector(xyz)
boat.colors = o3d.utility.Vector3dVector(rgb)
# o3d.visualization.draw_geometries([boat],
#                                   zoom=0.1,
#                                   front=[0, 0, -0.8795],
#                                   lookat=[0, 0, 0],
#                                   up=[0, -0.9768, 0.2024])

picked_id_source = pick_points(boat)
# custom_draw_geometry_with_custom_fov(boat, -90)
print(picked_id_source)
length = np.linalg.norm(xyz[picked_id_source[0]]-xyz[picked_id_source[1]])
print(length)
