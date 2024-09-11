[![manaakiwhenua-standards](https://github.com/manaakiwhenua/dggsBenchmarks/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

# DGGS benchmarks

Code written to generate DGGS benchmark cases, and measure their performance against non-DGGS GIS workflows.

Written to support: Law & Ardo (2024) "Using a discrete global grid system for a scalable, interoperable, and reproductible system of land-use classification" (In preparation.)

## Computer specifications

Processor: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz   2.50 GHz
Installed RAM: 32.0 GB (31.7 GB usable)
System type: 64-bit operating system, x64-based processor

## Executing benchmarks

Two Jupyter notebooks are available to generate and run benchmarking:

1. [Vector benchmarks](vector_benchmark.ipynb)
2. [Raster benchmarks](raster_benchmark.ipynb)

Benchmarking Notebooks are self documented, and they follow the same workflow as outlined in the paper:

1. Generation of Benchmark Data
2. (Indexing)
3. Joining
4. Classification

Local functions are defined within Jupyter Notebooks; benchmarks can also be found here

- [Vector functions](Vector_benchmarking/Vector_funcs.py)
- [DGGS functions (Vector)](Vector_benchmarking/DGGS_funcs.py)

- [Raster functions](Raster_benchmarking/Raster_funcs.py)
- [DGGS functions (Raster)](Raster_benchmarking/DGGS_funcs.py)
## Recorded benchmarking results


### Vector 
For vector experiments, each run and results of benchmarking are found in independent Jupyter notebooks, organised by number of inputs:


#### Vector (DGGS)

- [2](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_2.ipynb)
- [5](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_5.ipynb)
- [10](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_10.ipynb)
- [50](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_50.ipynb)
- [100](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_100.ipynb)
- [500](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_500.ipynb)
- [1000](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_1000.ipynb)

#### Vector (baseline)

- [2](Vector_benchmarking/Traditional/vector_join_classify_benchmark_2.ipynb)
- [5](Vector_benchmarking/Traditional/vector_join_classify_benchmark_5.ipynb)
- [10](Vector_benchmarking/Traditional/vector_join_classify_benchmark_10.ipynb)
- [50](Vector_benchmarking/Traditional/vector__join_classify_benchmark_50.ipynb)
- [100](Vector_benchmarking/Traditional/vector_join_classify_benchmark_100.ipynb)
- [250](Vector_benchmarking/Traditional/vector_join_classify_benchmark_250.ipynb)

##### Data for Vector & DGGS:

[Vector Data](Vector_benchmarking/Traditional/vector_1000)

[DGGS Data](Vector_benchmarking/DGGS/vector_1000)

### Raster

For raster experiments, data is contained within singular notebooks. The results for different numbers of inputs are in different cells.

#### Raster (DGGS)

- [Indexing](Raster_benchmarking/DGGS/Indexing.ipynb)
- [Joining and classifying](Raster_benchmarking/DGGS/join_classify.ipynb)

#### Raster (baseline)

- [Joining](Raster_benchmarking/Raster/stacking_join.ipynb)
- [Classifying](Raster_benchmarking/Raster/raster_classification.ipynb)