# Xsuite singularity images

This repository contains
definition files to build singularity images,
helper scripts
and examples
for running [Xsuite](https://xsuite.readthedocs.io) simulations on the GSI cluster.

The images are available at:
```
/cvmfs/aph.gsi.de/xsuite/
```
This folder contains several images in the form `xsuite_variant_YYYYMMDD.sif` and symbolic links (e.g. `xsuite.sif`) pointing to the latest image.
The variant `xsuite_amdrocm` is suited for the AMD GPUs used at GSI HPC.  
For usage documentation and general description please refer to: https://git.gsi.de/p.niedermayer/xsuite-on-hpc  
Further information on the provided images is available at: https://git.gsi.de/xsuite/xsuite-on-hpc/-/releases  

To build your own contianers using the definition files provided in this repository, use the `build` script or refer to https://hpc.gsi.de/virgo/user-guide/containers/build.html

## Getting started

If you use the containers provided, please star the repository at https://git.gsi.de/p.niedermayer/xsuite-on-hpc and subscribe to release notifications so as to be informed on important changes.

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
I recommend making copies of these scripts so that you can modify the parameters as well as the path to the singularity image.
It's a good idea to link to a specific container version such as `xsuite_amdrocm_20230908.sif` to prevent unexpected changes, instead of using the generic `xsuite.sif` which always points to the latest container.



**Run the example**
```bash
cp /cvmfs/aph.gsi.de/xsuite/example.py .

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
Singularity> ./example.py cpu
# --> Tracking completed in: 28.94 s
Singularity> ./example.py gpu
# --> Tracking completed in:  0.41 s

Singularity> exit
```

**Submit a job**

```bash
# Copy your script to the lustre storage
cd /lustre/$(id -ng)/$(id -nu)
cp /cvmfs/aph.gsi.de/xsuite/example.py .

# Submit it to the queue
xbatch example.py
```

It may take a while until the job is started. To check your job status:
```bash
xinfo
```

After the job has finished, the log file `example.py.slurm-JOBID.out` should look like this:
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


## Troubleshooting

<details>
<summary>No GPUs are shown or I get the error message "Could not find a GPU via the opencl context"</summary>

Check if GPUs are recognized by opencl at all with the `clinfo` command which is independent of pyopencl
```bash
Singularity> clinfo
...
Platform Name:                                   AMD Accelerated Parallel Processing
Number of devices:                               1
Device Type:                                     CL_DEVICE_TYPE_GPU
...
Platform Name:                                   Portable Computing Language
Number of devices:                               1
Device Type:                                     CL_DEVICE_TYPE_CPU
```

<details>
<summary>No, not recognized at all</summary>

Make sure you are using the slurm option `--gres=gpu` as is done by the [`xdebug`](scripts/xdebug) script.
See https://hpc.gsi.de/virgo/user-guide/examples/gpus.html for more details.

Also, check if you are member of the **video** group on virgo by using the `id` command (outside the container).  
If not, request access by sending an email to cluster-service@gsi.de with your username and the request to be added to the video group in order to use the AMD GPUs.

The `rocminfo` command (if available) might also provide useful hints.

</details>


<details>
<summary>Yes, clinfo does show a GPU</summary>

Then the issue is related to python.  
Make sure you are using the python installation of the singularity container. Since your `PATH` environment variable is adopted when you launch a container, make sure it does not link to a conflicting python installation (like miniconda).
```bash
Singularity> type python3
python3 is /usr/bin/python3
Singularity> echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/rocm/bin:/opt/rocm/opencl/bin
Singularity> echo $PYTHONPATH
    
```

</details>


</details>







*If your issue is not listed here, but you managed to solve it:  
Do your colleagues a favor and add it here (via merge request or mail to p.niedermayer@gsi.de)*



## Further reading
- High Performance Computing at GSI: https://hpc.gsi.de/virgo
- AMD ROCm GPUs at GSI: https://hpc.gsi.de/virgo/user-guide/examples/gpus.html#amd-rocm
- Slurm: https://slurm.schedmd.com/documentation.html
- Xsuite: https://xsuite.readthedocs.io
- List of GPU processors (gfx): https://llvm.org/docs/AMDGPUUsage.html
- AMD Accelerated Parallel Processing drivers: https://www.amd.com/en/support/linux-drivers
- Pyopencl: https://documen.tician.de/pyopencl/index.html
- CL compiler options: https://man.opencl.org/clBuildProgram.html


## Admin documentation

See [Wiki](https://git.gsi.de/p.niedermayer/xsuite-on-hpc/-/wikis)
