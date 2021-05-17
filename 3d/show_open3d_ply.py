import os
import pandas as pd
import open3d as o3d
import numpy as np
import cv2

ply_file = './test.ply'

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

# visualization of point clouds.
pcd = o3d.io.read_point_cloud('test.ply')
# o3d.visualization.draw_geometries([pcd])
o3d.visualization.draw_geometries([pcd],
                                  zoom=0.1,
                                  front=[0, 0, -0.8795],
                                  lookat=[0, 0, 0],
                                  up=[0, -0.9768, 0.2024])


