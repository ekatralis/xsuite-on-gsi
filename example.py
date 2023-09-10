#!/usr/bin/env python3

# Xsuite - A simple example
#
# Modified from: https://xsuite.readthedocs.io/en/latest/singlepart.html#a-simple-example

import numpy as np
import time
import sys

np.random.seed(2349875293)

import xobjects as xo
import xtrack as xt
import xpart as xp



## Context
####################

context = sys.argv[1] if len(sys.argv) > 1 else None

if context == 'cpu':
    context = xo.ContextCpu()

elif context == 'cupy':
    context = xo.ContextCupy()

elif context in ('opencl', 'gpu'):
    import pyopencl as cl    
    gpus = []
    print(f'OpenCL: available platforms ({len(cl.get_platforms())}):')
    for ip, platform in enumerate(cl.get_platforms()):
        print(f'  {ip} {platform.name} ({platform.vendor})\n'
              f'    {platform.version}')
        for id, device in enumerate(platform.get_devices()):
            typ = "GPU" if device.type == cl.device_type.GPU else "CPU"  if device.type == cl.device_type.CPU else "???"
            print(f'    {ip}.{id} {typ}: {device.name}')
            if device.type == cl.device_type.GPU:
                gpus.append(f'{ip}.{id}')
    if len(sys.argv) > 2:
        device = sys.argv[2]  # user selected device
    elif len(gpus) > 0:
        device = gpus[0]  # automatically use first gpu
    else:
        raise RuntimeError('Could not find a GPU via the opencl context. Use different context or specify device')

    print('Using device:', device, "\n")
    context = xo.ContextPyopencl(device)

else:
    context = None

if context is None:
    print('Usage: ./example.py [context] [device]')
    print('Available contexts: cpu, opencl, cupy')
    exit(1)

print()
print('Using context:', context)





## Setup
####################


## Generate a simple line
line = xt.Line(
    elements=[xt.Drift(length=2.),
              xt.Multipole(knl=[0, 1.], ksl=[0,0]),
              xt.Drift(length=1.),
              xt.Multipole(knl=[0, -1.], ksl=[0,0])],
    element_names=['drift_0', 'quad_0', 'drift_1', 'quad_1'])

## Transfer lattice on context and compile tracking code
line.build_tracker(_context=context)

## Build particle object on context
n_part = int(1e6)
particles = xp.Particles(_context=context,
                        p0c=6500e9,
                        x=np.random.uniform(-1e-3, 1e-3, n_part),
                        px=np.random.uniform(-1e-5, 1e-5, n_part),
                        y=np.random.uniform(-2e-3, 2e-3, n_part),
                        py=np.random.uniform(-3e-5, 3e-5, n_part),
                        zeta=np.random.uniform(-1e-2, 1e-2, n_part),
                        delta=np.random.uniform(-1e-4, 1e-4, n_part),
                        )



## Tracking
####################


## Track (saving turn-by-turn data)
n_turns = int(1e3)
print(f'Tracking {n_part:g} particles over {n_turns:g} turns...'); t = time.perf_counter()

line.track(particles, num_turns=n_turns,
#           turn_by_turn_monitor=True
)

context.synchronize() # wait for completion (mandatory for CuPy context)

print('Tracking completed in:', time.perf_counter()-t, 's')

## Turn-by-turn data is available at:
#print(particles.x)
# etc...

## Check if it worked
x = context.nparray_from_context_array(particles.x)
assert n_part == int(1e6) and n_turns == int(1e3) and np.allclose(x[:3], [-9.40795199e-05,  1.12466795e-04, -2.97543231e-05])
print('Test passed')

