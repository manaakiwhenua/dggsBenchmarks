from functools import partial
from math import sqrt
from pathlib import Path
import geopandas as gpd
import h3pandas
from itertools import product
import time
import timeit
import csv
import matplotlib.pyplot as plt  # Ensure you import matplotlib for plotting

def benchmark_gpkg_files(input_dir, output_dir, num_files_to_open, bench_runs, h3_res=14):

    # Get a list of all GPKG files in the folder
    v_files = list(sorted(input_dir.glob('*.gpkg')))

    # Initialize lists to store benchmarking times
    indexing_time = []
    joining_time = []

    def run_loop(num_files_to_open, v_files, h3_res):
        index_time = []
        join_time = []

        start_time = time.time()
        for i, file in enumerate(v_files[:num_files_to_open]):
            col_name = file.stem.split('_')[1]  # Extracting the column name from the file name
            df = gpd.read_file(file).to_crs(4326)

            # Indexing benchmark
            index_Stime = time.time()
            df = df.h3.polyfill(h3_res, explode=True).drop(columns=['geometry'])
            index_Etime = time.time()
            index_Ftime = index_Etime - index_Stime
            index_time.append(index_Ftime)

            # Joining benchmark
            join_Stime = time.time()
            df.columns = [col_name, *df.columns[1:]]  # Setting the column to the file
            df = df.set_index('h3_polyfill')
            if i == 0:
                combined_df = df.copy()
            else:
                combined_df = combined_df.join(df)
            join_Etime = time.time()
            join_Ftime = join_Etime - join_Stime
            join_time.append(join_Ftime)

        # Calculate and print the time taken for each run
        end_time = time.time()
        time_taken = end_time - start_time

        indexing_time.append(sum(index_time))
        joining_time.append(sum(join_time))
        print(f'Run: index time - {sum(index_time)} seconds, joining time - {sum(join_time)} seconds, Total time- {time_taken} seconds')

    # Run the benchmark
    timeit.timeit(lambda: run_loop(num_files_to_open, v_files, h3_res), number=bench_runs)


def load_and_prepare_data(input_dir, num_files_to_open, h3_res):
    # Get a list of all GPKG files in the folder
    v_files = list(sorted(input_dir.glob('*.gpkg')))
    combined_df = None

    for i, file in enumerate(v_files[:num_files_to_open]):
        col_name = file.stem.split('_')[1]  # Extracting the column name from the file name
        df = gpd.read_file(file).to_crs(4326)
        df = df.h3.polyfill(h3_res, explode=True).drop(columns=['geometry'])
        df.columns = [col_name, *df.columns[1:]]  # Setting the column to the file
        df = df.set_index('h3_polyfill')
        if i == 0:
            combined_df = df.copy()
        else:
            combined_df = combined_df.join(df)

    return combined_df

def define_classes():
    def is_prime(n):
        if n <= 1 or not isinstance(n, int):
            return False
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def is_polygonal(s, x):
        assert s > 2 and isinstance(s, int) and isinstance(x, int)
        n = (sqrt(8 * (s - 2) * x + (s - 4) ** 2) + (s - 4)) / (2 * (s - 2))
        return n.is_integer()

    def is_fibonacci(n):
        if not isinstance(n, int) or n < 0:
            return False
        a, b = 0, 1
        while a < n:
            a, b = b, a + b
        return a == n

    def is_perfect(n):
        if n < 2 or not isinstance(n, int):
            return False
        total = 1
        i = 2
        while i * i <= n:
            if n % i == 0:
                total += i + n // i
            i += 1
        return total == n

    classes = [
        ('is_prime', is_prime),
        ('is_triangular', partial(is_polygonal, 3)),
        ('is_rectangular', partial(is_polygonal, 4)),
        ('is_pentagonal', partial(is_polygonal, 5)),
        ('is_hexagonal', partial(is_polygonal, 6)),
        ('is_fibonacci', is_fibonacci),
        ('is_perfect', is_perfect),
    ]

    return classes

def apply_classifications(combined_df, classes):
    combined_df['sum'] = combined_df.select_dtypes(include='number').sum(axis=1)
    
    # Ensure 'sum' column is filled and converted to integers
    combined_df['sum'] = combined_df['sum'].fillna(0).astype(int)

    for name, func in classes:
        combined_df[name] = combined_df['sum'].apply(func)

    numerics = list(combined_df.select_dtypes(include='number'))
    combined_df = combined_df.drop(columns=numerics)

    return combined_df

def benchmark_classification(combined_df, bench_runs):
    classify_time = []

    # Adjusting for actual boolean combinations
    combinations = list(product([0, 1], repeat=len(combined_df.columns)))
    class_mapping = {tuple(row): f'Class_{i+1:03}' for i, row in enumerate(combinations)}
    
    def classify_loop():
        start_time = time.time()

        # Classification process
        bench_class = combined_df.apply(lambda row: class_mapping[tuple(row)], axis=1)

        end_time = time.time()

        # Calculate and print the time taken for each run
        time_taken = end_time - start_time
        classify_time.append(time_taken)
        print(f'Run: Time taken - {time_taken} seconds')

    timeit.timeit(lambda: classify_loop(), number=bench_runs)

def final_processing_and_plotting(combined_df, class_mapping):
    # Apply the final classification to create the 'class' column
    combined_df['class'] = combined_df.apply(lambda row: class_mapping[tuple(row.astype(int))], axis=1)

    # Create a GeoDataFrame for H3 geometries
    h3_df = combined_df[['class']]
    h3_df = h3_df.h3.h3_to_geo_boundary()

    # Dissolve by 'class' and reproject to CRS 2193
    h3_df = h3_df.dissolve(by='class').reset_index().to_crs(2193)

    # Plot the results
    h3_df.plot('class', cmap='viridis')
    plt.show()