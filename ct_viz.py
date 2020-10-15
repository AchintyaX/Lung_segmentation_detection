import SimpletITK as sitk 
import matplotlib.pyplot as plt 
%matplotlib inline 

import numpy as np
from skimage import measure, feature
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Ensure that we have both .mhd and .raw files for the ct_scan in the same directory 

class ct_visualization:
    def __init__(self, path):
        self.path = path
    
        self.data = sitk.ReadImage(self.path)
        self.spacing = self.data.GetSpacing()
        self.scan = sitk.GetArrayFromImage(self.data)

    # plotting all the 2D slices for a ct-scan
    def plot_ct_scan(self, num_column=4, jump=1):
    	# counting the number of slices for the scan
        num_slices = len(self.scan)
        num_row = (num_slices//jump + num_column - 1) // num_column
        f, plots = plt.subplots(num_row, num_column, figsize=(num_column*5, num_row*5))
        for i in range(0, num_row*num_column):
            plot = plots[i % num_column] if num_row == 1 else plots[i // num_column, i % num_column]        
            plot.axis('off')
            if i < num_slices//jump:
                plot.imshow(self.scan[i*jump], cmap=plt.cm.bone) 

                
    def plot_3d(self, threshold=-400):
    
        # Position the scan upright, 
        # so the head of the patient would be at the top facing the camera
        p = self.scan.transpose(2,1,0)
        # p = p[:,:,::-1]
    
        verts,faces = measure.marching_cubes_classic(p, threshold)

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Fancy indexing: `verts[faces]` to generate a collection of triangles
        mesh = Poly3DCollection(verts[faces], alpha=0.1)
        face_color = [0.5, 0.5, 1]
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)

        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[1])
        ax.set_zlim(0, p.shape[2])

        plt.show()
