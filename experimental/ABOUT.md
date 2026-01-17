# ROCm-7 container

The container can be built with two different cupy distributions that are built for ROCm 7.x. 
- CuPy `v14.0.0rc1` distributed from CuPy's pre-release PyPI index https://pip.cupy.dev/pre:
    ```bash
    apptainer build --build-arg CUPY_SOURCE='PYPI' ./rocm7test.sif ./rocm_7_xs.def
    ```
- CuPy `v.13.5.1` distributed from AMD's PyPI index https://pypi.amd.com/rocm-7.0.2/simple:
    ```bash
    apptainer build --build-arg CUPY_SOURCE='AMD' ./rocm7test.sif ./rocm_7_xs.def
    ```
If no build argument is passed, the AMD PyPI index is used.