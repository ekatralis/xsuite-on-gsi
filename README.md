# Xsuite singularity images

We provide the following singularity images for [Xsuite](https://xsuite.readthedocs.io):

- **AMD** Radeon GPU image  
  ```
  /cvmfs/aph.gsi.de/xsuite/xsuite.sif
  ```

Please refer to https://git.gsi.de/p.niedermayer/xsuite-on-hpc for usage documentation

## Getting started

*This guide was written on 2023-03-21 by p.niedermayer@gsi.de*

**Login to GSI High-Performance Computing (HPC)**  
If you do not have an account, read [this](https://hpc.gsi.de/virgo/introduction/request_access.html)
```bash
ssh virgo2.hpc.gsi.de
```

**Add scripts to your path**  
A number of scripts are provided to help submitting jobs for Xsuite to the **GPU** nodes.
```bash
echo 'PATH=$PATH:/cvmfs/aph.gsi.de/xsuite/scripts/' >> ~/.bashrc
```

**Run the example**
```bash
# Start an interactive session for testing
xdebug

# List installed software versions
Singularity> pip list | grep -E "(^x|numpy|scipy|plot)"

# List available GPUs
Singularity> python3 -c 'import xobjects as xo;xo.ContextPyopencl.print_devices()'
Context 0: AMD Accelerated Parallel Processing
Device 0.0: gfx906:sramecc+:xnack-                    # <-- this is the GPU (gfx906 = AMD Radeon Instinct MI50)
Context 1: Portable Computing Language
Device 1.0: pthread-AMD EPYC 7551 32-Core Processor   # <-- this is the CPU

# Run the example
Singularity> /cvmfs/aph.gsi.de/xsuite/example.py cpu
# --> Tracking completed in: 2.285 s
Singularity> /cvmfs/aph.gsi.de/xsuite/example.py gpu
# --> Tracking completed in: 0.094 s
```

**Submit a job**
```bash
xbatch /cvmfs/aph.gsi.de/xsuite/example.py
```

It may take a while until the job is started. To check your job status:
```bash
xinfo
```

After the job has finished, the log should look like this:
```txt
OpenCL: available platforms (2):
  0 AMD Accelerated Parallel Processing (Advanced Micro Devices, Inc.)
    OpenCL 2.1 AMD-APP (3452.0)
    0.0 GPU: gfx908:sramecc+:xnack-
    0.1 GPU: gfx908:sramecc+:xnack-
    0.2 GPU: gfx908:sramecc+:xnack-
    0.3 GPU: gfx908:sramecc+:xnack-
    0.4 GPU: gfx908:sramecc+:xnack-
    0.5 GPU: gfx908:sramecc+:xnack-
    0.6 GPU: gfx908:sramecc+:xnack-
    0.7 GPU: gfx908:sramecc+:xnack-
  1 Portable Computing Language (The pocl project)
    OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG
    1.0 CPU: pthread-AMD EPYC 7413 24-Core Processor
Using device: 0.0


Using context: <xobjects.context_pyopencl.ContextPyopencl object at 0x7f9b21cacb50>
Tracking 1e+06 particles over 1000 turns...
Tracking completed in: 0.277615818195045 s
[-9.40795199e-05  1.12466795e-04 -2.97543231e-05 ... -3.90585592e-04
  5.41514519e-04  6.29759048e-04]

real    0m4.323s
user    0m2.987s
sys     0m0.758s
```



## Further reading
- High Performance Computing at GSI: https://hpc.gsi.de/virgo
- Slurm documentation: https://slurm.schedmd.com/documentation.html
- Xsuite: https://xsuite.readthedocs.io
- List of GPU processors (gfx): https://llvm.org/docs/AMDGPUUsage.html
- AMD Accelerated Parallel Processing drivers: https://www.amd.com/en/support/linux-drivers
- Pyopencl docs: https://documen.tician.de/pyopencl/index.html
- CL compiler options: https://man.opencl.org/clBuildProgram.html


