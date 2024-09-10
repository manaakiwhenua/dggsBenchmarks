[![manaakiwhenua-standards](https://github.com/manaakiwhenua/dggsBenchmarks/workflows/manaakiwhenua-standards/badge.svg)](https://github.com/manaakiwhenua/manaakiwhenua-standards)

# DGGS benchmarks

Code written to generate DGGS benchmark cases, and measure their performance against non-DGGS GIS workflows.

Written to support: Law & Ardo (2024) "Using a discrete global grid system for a scalable, interoperable, and reproductible system of land-use classification" (In preparation.)

## Computer specifications
Processor: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz   2.50 GHz
Installed RAM: 32.0 GB (31.7 GB usable)
System type: 64-bit operating system, x64-based processor

## To run benchmarks

Two ([vector_benchmark](vector_benchmark.ipynb) and [raster_benchmark](raster_benchmark.ipynb)) jupyter notebooks are available to generate and run benchmarking.

Benchmarking notebooks are self explanatory, they  follow the same workflow as outlined in the paper:

Generation of Benchmark Data -> (Indexing) -> Joining -> Classification

#### Local functions are defined within python codes for Vector benchmarking can be found:
[Vector functions](Vector_benchmarking/Vector_funcs.py)

[DGGS functions](Vector_benchmarking/DGGS_funcs.py)


## Paper benchmarks results

Data and benchmark results for the paper can be found within this repository.

#### Each run and results of benchmarking for Vector & DGGS can be found in independent jupyter notebooks within the folder:

Vector_benchmarking/DGGS/dggs_join_classify_benchmark_
[2](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_2.ipynb)
[5](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_5.ipynb)
[10](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_10.ipynb)
[50](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_50.ipynb)
[100](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_100.ipynb)
[500](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_500.ipynb)
[1000.ipynb](Vector_benchmarking/DGGS/dggs_join_classify_benchmark_1000.ipynb)

Vector_benchmarking/Traditional/vector_join_classify_benchmark_
[2](Vector_benchmarking/Traditional/vector_join_classify_benchmark_2.ipynb)
[5](Vector_benchmarking/Traditional/vector_join_classify_benchmark_5.ipynb)
[10](Vector_benchmarking/Traditional/vector_join_classify_benchmark_10.ipynb)
[50](Vector_benchmarking/Traditional/vector__join_classify_benchmark_50.ipynb)
[100](Vector_benchmarking/Traditional/vector_join_classify_benchmark_100.ipynb)
[250.ipynb](Vector_benchmarking/Traditional/vector_join_classify_benchmark_250.ipynb)

#### Data for Vector & DGGS:

[Vector Data](Vector_benchmarking/Traditional/vector_1000)

[DGGS Data](Vector_benchmarking/DGGS/vector_1000)