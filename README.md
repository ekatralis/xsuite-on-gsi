# Xsuite singularity images


This repository contains
definition files to build singularity images,
helper scripts
and examples
for running [Xsuite](https://xsuite.readthedocs.io) simulations on the GSI cluster.

**Prebuild images**

Prebuild images are available via APH CVMFS in the xsuite folder at:
```
/cvmfs/aph.gsi.de/xsuite/
```
This folder contains several images in the form `xsuite_variant_YYYYMMDD.sif` and symbolic links (e.g. `xsuite.sif`) pointing to the latest image.
The variants `xsuite_amdrocm` and `xsuite_amdopencl` are suited for the AMD GPUs used at GSI HPC.
- The variant `xsuite_amdrocm` includes the full rocm stack, which results in a larger container. It provides both `ContextCupy` and `ContextPyopencl` on AMD GPUs.
- The variant `xsuite_amdopencl` includes only the rocm components linked to OpenCL. It provides only `ContextPyopencl`

For usage documentation and general description please refer to https://git.gsi.de/p.niedermayer/xsuite-on-hpc and https://git.gsi.de/xsuite/xsuite-on-hpc/-/releases  

**Build your own image**

To build your own container image using the definition files provided in this repository:
```bash
ssh virgo.hpc.gsi.de
$ git clone git@git.gsi.de:xsuite/xsuite-on-hpc.git
$ cd xsuite-on-hpc
$ ./build xsuite_amdrocm.def
```
Refer to https://hpc.gsi.de/virgo/user-guide/containers/build.html for a detailed description.

## Getting started

If you use the containers provided, please star the repository at https://git.gsi.de/p.niedermayer/xsuite-on-hpc and subscribe to release notifications so as to be informed on important changes.

*This guide was last updated on 2025-04-08 by p.niedermayer@gsi.de*

**Login to GSI High-Performance Computing (HPC)**  
If you do not have an account, contact your appartements coordinator (see [FAQ](https://hpc.gsi.de/virgo/help/faq))
```bash
ssh virgo.hpc.gsi.de
```
Then change to your lustre folder (only the lustre file system will be accessible from the job nodes):
```bash
export LUSTRE_HOME=/lustre/$(id -ng)/$(id -nu)
cd $LUSTRE_HOME
```
And create a script (here we just copy the example and make sure it's executable):
```bash
cp /cvmfs/aph.gsi.de/xsuite/example.py .
chmod a+x example.py
```

**Start an interactive session**

Run an interactive session (pty) on the GPU partition with all 8 GPUs available per node, and use the xsuite singularity image:
```bash
srun --partition=gpu --gres=gpu:8 --pty -- singularity shell /cvmfs/aph.gsi.de/xsuite/xsuite.sif
```

Once the node is allocated, check the software versions (always a good idea to test locally with exactly the same versions to avoid suprises):
```bash
python --version
pip list | grep -Ei "(^x|mad|numpy|scipy)"
```

Check the available contexts for running xsuite simulations:
```bash
python3 -c 'import xobjects as xo;xo.ContextPyopencl.print_devices()'
```
> This will print something like the following, where you can see the 8 GPUs (gfx908 is the AMD Readon Instinct MI100) as well as the CPU
> ```text
> Platform 0  : AMD Accelerated Parallel Processing
> Device   0.0: gfx908:sramecc+:xnack-
> Device   0.1: gfx908:sramecc+:xnack-
> Device   0.2: gfx908:sramecc+:xnack-
> Device   0.3: gfx908:sramecc+:xnack-
> Device   0.4: gfx908:sramecc+:xnack-
> Device   0.5: gfx908:sramecc+:xnack-
> Device   0.6: gfx908:sramecc+:xnack-
> Device   0.7: gfx908:sramecc+:xnack-
> Platform 1  : Portable Computing Language
> Device   1.0: cpu-haswell-AMD EPYC 7413 24-Core Processor
> ```


**Run the example script**

Since we just copied the script to our lustre home, it is mounted in the image and we can simply execute it:
```bash
./example.py gpu
```
> This runs the example tracking on a single GPU, which is very fast
> ```text
> Using context: ContextPyopencl:0.0
> Tracking 1e+06 particles over 1000 turns...
> Tracking completed in: 0.39723753998987377 s
> Test passed
> ```
To compare with, the same tracking executed on CPU:
```bash
./example.py cpu
```
> ```text
> Using context: ContextCpu
> Tracking 1e+06 particles over 1000 turns...
> Tracking completed in: 87.2150330208242 s
> Test passed
> ```

Finally log out
```bash
exit
```


**Job submission**  
Normally, you want to submit jobs non-interactively. To help doning so, we provide a number of scripts.
Copy them to your personal folder and adjust them to your needs (if required):
```bash
mkdir $LUSTRE_HOME/scripts
cp /cvmfs/aph.gsi.de/xsuite/scripts/* $LUSTRE_HOME/scripts/
chmod a+x $LUSTRE_HOME/scripts/*
echo "PATH=\$PATH:$LUSTRE_HOME/scripts/" >> ~/.bashrc
# Log out and back in for this to take effect
```
To prevent unexpected changes when we update the images, it's a good idea to pin the container used by the scripts, i.e. change the generic `xsuite.sif` to a specific version such as `xsuite_amdrocm_20250408.sif` and adjust the paths in the scripts to point to your local copy.

Then you can copy your scripts to lustre (we'll use the example script from above) and submit a job:
```bash
cd $LUSTRE_HOME
# example.py already copied (see above)
xbatch example.py gpu
```

This will start monitoring the job's logfile `example.py.slurm-JOBID.out` for your convenience, press CTRL-C to leave the job alone. To check your job status later run:
```bash
xinfo
```

After the job has finished, the log file should look like this:
```txt
OpenCL: available platforms (2):
  0 AMD Accelerated Parallel Processing (Advanced Micro Devices, Inc.)
    OpenCL 2.1 AMD-APP (3635.0)
    0.0 GPU: gfx908:sramecc+:xnack-
    0.1 GPU: gfx908:sramecc+:xnack-
    0.2 GPU: gfx908:sramecc+:xnack-
    0.3 GPU: gfx908:sramecc+:xnack-
    0.4 GPU: gfx908:sramecc+:xnack-
    0.5 GPU: gfx908:sramecc+:xnack-
    0.6 GPU: gfx908:sramecc+:xnack-
    0.7 GPU: gfx908:sramecc+:xnack-
  1 Portable Computing Language (The pocl project)
    OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, DISTRO, POCL_DEBUG
    1.0 CPU: cpu-haswell-AMD EPYC 7413 24-Core Processor
Using device: 0.0


Using context: ContextPyopencl:0.0
Tracking 1e+06 particles over 1000 turns...
Tracking completed in: 0.4085924569517374 s
Test passed

real    0m9.761s
user    0m5.873s
sys     0m1.221s
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
