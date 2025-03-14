import open3d as o3d
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Open a file dialog for user to select the file
root = tk.Tk()
root.withdraw()  # Hide the root window
file_path = filedialog.askopenfilename(
    title="Select a 3D File",
    filetypes=[("3D Files", "*.ply *.obj *.stl *.pcd"), ("All Files", "*.*")])

if not file_path:
    print("No file selected. Exiting...")
    exit()

if file_path.endswith(".pcd"):
    pcd = o3d.io.read_point_cloud(file_path)
    if pcd.is_empty():
        print("The point cloud file is empty or corrupted.")
        exit()
    # Normalize the point cloud for better visualization
    pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()), center=pcd.get_center())

    # Correct flipped axes if needed
    bbox = pcd.get_axis_aligned_bounding_box()
    if (bbox.max_bound < bbox.min_bound).any():
        bbox.min_bound, bbox.max_bound = np.minimum(bbox.min_bound, bbox.max_bound), np.maximum(bbox.min_bound, bbox.max_bound)

    pcd.paint_uniform_color([0.1, 0.9, 0.1])  # Example color
    o3d.visualization.draw([pcd], show_ui=True)

else:
    print("Selected file format is not supported for visualization.")