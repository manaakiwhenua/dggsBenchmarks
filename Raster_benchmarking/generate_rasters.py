import os
import numpy as np
import random
import sys
from nlmpy import nlmpy

def generate_nlm_rasters(output_dir, nRow=100, nCol=100, layers=10000, cellSize=10, seed=0):

    np.random.seed(seed)  # Ensure reproducibility for NLMs
    random.seed(seed)     # Seed for jittering output rasters
    
    # Ensure output directory exists for discrete and continuous rasters
    discrete_dir = os.path.join(output_dir, "discrete")
    continuous_dir = os.path.join(output_dir, "continuous")
    os.makedirs(discrete_dir, exist_ok=True)
    os.makedirs(continuous_dir, exist_ok=True)

    # Function to create raster metadata
    def raster_metadata(cellSize):
        return {
            'xll': 1743159.15 + 10 * random.uniform(-1, 1),
            'yll': 5469287.46 + 10 * random.uniform(-1, 1),
            'cellSize': cellSize
        }

    # Generate discrete rasters
    for layer in range(layers):
        nlm = nlmpy.mpd(nRow, nCol, 0.75)
        nlm = nlmpy.classifyArray(nlm, np.random.randint(1, 11, (1, 10))).astype(int)
        nlmpy.exportASCIIGrid(os.path.join(discrete_dir, f'raster-{layer}.asc'), nlm, **raster_metadata(cellSize))

    # Generate continuous rasters
    for layer in range(layers):
        nlm = nlmpy.mpd(nRow, nCol, 0.75)
        nlmpy.exportASCIIGrid(os.path.join(continuous_dir, f'raster-{layer}.asc'), nlm, **raster_metadata(cellSize))