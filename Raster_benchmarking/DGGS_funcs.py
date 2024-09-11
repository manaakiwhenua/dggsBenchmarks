from numba import jit
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from joblib import Parallel, delayed
import polars as pl
import numpy as np
import h3pandas
from joblib import Parallel, delayed
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt 


def h3index_raster(file, output_dir, h3_res=12, stem=None, operation='max'):
    import h3pandas # https://github.com/DahnJ/H3-Pandas/issues/27
    with rasterio.open(file) as src:
        array = src.read(1)
        transform = src.transform
    array[np.isnan(array)] = 0
    height, width = array.shape
    cols, rows = np.meshgrid(np.arange(width), np.arange(height), indexing='xy')
    xs, ys = rasterio.transform.xy(transform, rows.flatten(), cols.flatten(), offset='center')
    dstack = np.dstack((xs, ys))[0]
    pts = [Point(*c) for c in dstack]
    df = gpd.GeoDataFrame(zip(array.flatten(), pts), columns=['value','geometry'], crs='EPSG:2193')
    df = df.to_crs(4326)
    df = df.h3.geo_to_h3_aggregate(h3_res, operation=operation, return_geometry=False)
    df.to_parquet(f'{output_dir}/{stem}_{file.stem}.parquet', index=f'h3_{h3_res}')


def process_file(i, file, scale=1):
    """Processes a single file, scaling values and checking for primes."""
    # Read the parquet file
    df = pl.read_parquet(file)
       
    # Add the prime boolean to the DataFrame
    if df['value'].dtype.is_integer():
        scaled = (df['value'] * scale)
    else:
        scaled = (df['value'] * scale).floor()
    
    #Defining functions
    @np.vectorize
    def is_prime(n):
        if n == 1: return 0
        if n % 2 == 0 and n > 2:
            return 0
        return int(all(n % i for i in range(3, int(np.sqrt(n)) + 1, 2)))

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

    funcs = [
        is_prime,
        is_triangular, is_rectangular, is_pentagonal, is_hexagonal,
        is_fibonacci,
        is_perfect
    ]

    for func in funcs:
        f = lambda v: int(func(v))
        df = df.with_columns([
            pl.Series(f"{func.__name__}_{i}", scaled.map_elements(f, return_dtype=int))
        ])
    df = df.drop("value")
    df = df.with_columns(sum=pl.sum_horizontal(df.columns[1:]))[["h3_12","sum"]]
    df = df.rename({"sum": f"sum_{i}"})
    return df


def classify(files, N, scale=1):
    # Process files in parallel
    dfs = Parallel(n_jobs=-1)(delayed(process_file)(i, file, scale) for i, file in enumerate(tqdm(files[:N], desc="Processing files")))

    final_df = dfs[0]

    # Join all DataFrames on the "h3_12" column
    for i, df in enumerate(tqdm(dfs[1:], desc="Joining DataFrames")):
        final_df = final_df.join(df, on="h3_12", how="outer_coalesce")

    return final_df

def summing(df):
    return df.with_columns(sum=pl.sum_horizontal(df.columns[1:]))[["h3_12","sum"]]

def final_plotting(combined_df):

    cont_df= combined_df.to_pandas().set_index('h3_12')
    
    h3_df = cont_df.h3.h3_to_geo_boundary()

    h3_df = h3_df.dissolve(by='sum').reset_index().to_crs(2193)

    h3_df.plot('sum', cmap='viridis')
    plt.show()