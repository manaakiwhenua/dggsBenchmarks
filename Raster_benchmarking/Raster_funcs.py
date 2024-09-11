import numpy as np
import math
from pathlib import Path
import rasterio
from rasterio.plot import show_hist
from rasterio.dtypes import int16, uint8, float64
from rasterio.enums import Resampling
from pathlib import Path
import numpy as np
from rasterio.crs import CRS
import rasterio.warp
import os
EPSG2193 = CRS.from_epsg(2193)

def process_rasters(input_dir, number_of_files, output_file='output.tif', nodata=0, dtype=np.uint8, resampling=Resampling.nearest):
    # Get sorted list of raster files from the input directory
    raster_files = list(sorted(Path(input_dir).glob('*.asc')))
    
    # Limit the number of files processed to the specified amount
    raster_files = raster_files[:number_of_files]

    if not raster_files:
        raise ValueError("No files found in the specified directory.")

    # Take the first raster as a template
    with rasterio.open(raster_files[0], 'r') as src:
        src_transform = src.transform
        src_profile = src.profile

    # Update the profile for the output GeoTIFF
    src_profile.update(driver='GTiff')  # Upgrade from ASC to GeoTIFF
    src_profile.update(crs=EPSG2193)  # Declare (missing) EPSG
    src_profile.update(count=len(raster_files))  # Make room for all bands

    # Align and write the output to a single multi-band GeoTIFF file
    with rasterio.open(output_file, 'w', **src_profile) as dst:
        for band, raster_file in enumerate(raster_files):
            with rasterio.open(raster_file, 'r') as src:
                data, transform = rasterio.warp.reproject(
                    source=src.read(1),
                    destination=np.zeros((1, src.height, src.width), dtype=dtype),
                    src_transform=src.transform,
                    dst_transform=src_transform,
                    src_crs=EPSG2193,
                    dst_crs=EPSG2193,
                    dst_nodata=nodata,
                    resampling=resampling
                )
                dst.write(data[0], band + 1)


def compute(input_file, dtype=int16, scale=100, band_limit=None):

    @np.vectorize
    def is_prime(n):
        if n % 2 == 0 and n > 2:
            return False
        return all(n % i for i in range(3, int(np.sqrt(n)) + 1, 2))

    @np.vectorize
    def is_polygonal(s, x):
        assert s > 2 and s % 1 == 0 and x % 1 == 0
        n = (np.sqrt(8 * (s - 2) * x + (s - 4) ** 2) + (s - 4)) / (2 * (s - 2))
        return n % 1 == 0

    @np.vectorize
    def is_fibonacci(n):
        a, b = 0,1
        while a < n:
            a, b = b, a + b
        return a == n

    @np.vectorize
    def is_perfect(n):
        sum = 1
        i = 2
        while i * i <= n:
            if n % i == 0:
                sum = sum + i + n/i
            i += 1
        return sum == n and n != 1

    def is_triangular(n):
        return is_polygonal(3, n)
        
    def is_rectangular(n):
        return is_polygonal(4, n)

    def is_pentagonal(n):
        return is_polygonal(5, n)

    def is_hexagonal(n):
        return is_polygonal(6, n)

    # Calculate whether each value in each band satisfies a function
    # Then count the number of times it satisfies the function, and write that out

    funcs = [
        is_prime,
        is_triangular, is_rectangular, is_pentagonal, is_hexagonal,
        is_fibonacci,
        is_perfect
    ]

    with rasterio.open(input_file, 'r') as src:
        shape = (src.indexes[-1], *src.shape)
        for func in funcs:
            src_profile = src.profile.copy()
            output = np.zeros(shape, dtype)
            for band in src.indexes[:band_limit]:
                data = src.read(band)
                data *= scale
                output[band-1] = func(data.astype(dtype))
    
            src_profile.update(count=1)
            src_profile.update(dtype=dtype)
            count_satisfaction = np.apply_along_axis(np.sum, 0, output)
            with rasterio.open(Path(f'Raster_benchmarking/data/raster/{input_file.stem}-{func.__name__}-{(band_limit or len(src.indexes))}.tif'), 'w', **src_profile) as dst:
                dst.write(count_satisfaction, 1)