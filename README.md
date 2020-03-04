# biorobots_1.6.1_reproducible

In this project, we address reproducibility issues with PhysiCell 1.6.1 for the biorobots sample project.

First, to address the issue of non-determinism in the OpenMP scheduler, we replace:
```
#pragma omp parallel for
```
with
```
#pragma omp parallel for schedule(static)
```

Second, to address the non-determinism of the PRNG in a multi-threaded environment, we create a PRNG for each thread and provide a unique seed for each one.

Third, we fix a race condition.
