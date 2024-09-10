from functools import partial
from math import sqrt
from pathlib import Path
import geopandas as gpd
from itertools import product
import time
import timeit
import csv

# Loop through each GPKG file and join

input_dir = Path('.\Vector_benchmarking\data')
output_dir = Path.cwd()
num_files_to_open = 20 #Change to desired input number
benchmark_runs = 5 #Change to desired benchmark runs
h3_res = 14 #Change to desired h3 resolution


def benchmark_vector_join(input_dir, output_dir, num_files_to_open, bench_runs, h3_res=14):
    # Get a list of all GPKG files in the folder
    v_files = list(sorted(input_dir.glob('*.gpkg')))

    # Initialize lists to store benchmarking times
    indexing_time = []
    joining_time = []

    def run_loop(num_files_to_open, v_files, h3_res):
        join_times = []

        start_time = time.time()
        for i, file in enumerate(v_files[:num_files_to_open]):
            # Extract column name from file name
            col_name = file.stem.split('_')[1]
            df = gpd.read_file(file)
            df.columns = [col_name, *df.columns[1:]]

            # Joining benchmark
            join_start_time = time.time()
            if i == 0:
                combined_df = df.copy()
            else:
                combined_df = gpd.overlay(combined_df, df)
            join_end_time = time.time()

            join_times.append(join_end_time - join_start_time)

        # Calculate and print the time taken for each run
        end_time = time.time()
        time_taken = end_time - start_time

        joining_time.append(sum(join_times))
        print(f'Run: joining time - {sum(join_times):.2f} seconds, Total time - {time_taken:.2f} seconds')

    # Run the benchmark
    timeit.timeit(lambda: run_loop(num_files_to_open, v_files, h3_res), number=bench_runs)


def load_and_prepare_vectors(input_dir, num_files_to_open):
    v_files = list(sorted(input_dir.glob('*.gpkg')))
    for i, file in enumerate(v_files[:num_files_to_open]):
        col_name = file.stem.split('_')[1]  # Extracting the column name from the file name
        df = gpd.read_file(file)
        df.columns = [col_name, *df.columns[1:]] #Setting the column to the file
        if i == 0:
            combined_df = df.copy()
        else:
            combined_df = gpd.overlay(combined_df, df)
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
        
def apply_classification_vector(combined_df,classes):
    combined_df['sum'] = combined_df.select_dtypes(include='number').sum(axis=1)
    for i, func in enumerate(classes):
        combined_df[func[0]] = combined_df['sum'].apply(func[1])
    return combined_df

def benchmark_classification_vector(combined_df, bench_runs):

    classify_time = []  # Initialize the list to store classification times

    # Adjusting for actual boolean combinations
    combinations = list(product([True, False], repeat=7))
    class_mapping = {tuple(row): f'Class_{i+1:03}' for i, row in enumerate(combinations)}

    def classify_loop():
        start_time = time.time()

        bench_class = combined_df[['is_prime','is_triangular','is_rectangular','is_pentagonal','is_hexagonal','is_fibonacci','is_perfect']].apply(lambda row: class_mapping[tuple(row.astype(int))], axis=1) #This should remain the same, as cell count remains static   

        end_time = time.time()
        
        # Calculate and print the time taken for each run
        time_taken = end_time - start_time
        classify_time.append(time_taken)
        print(f'Run: Time taken - {time_taken} seconds')

    # Run the benchmark
    timeit.timeit(lambda: classify_loop(), number=bench_runs)

def final_processing_and_plotting_v(combined_df, class_mapping):
    combined_df['class'] = combined_df[['is_prime','is_triangular','is_rectangular','is_pentagonal','is_hexagonal','is_fibonacci','is_perfect']].apply(lambda row: class_mapping[tuple(row.astype(int))], axis=1)
    combined_df=combined_df[['class','geometry']]
    combined_df.plot('class', cmap='viridis')