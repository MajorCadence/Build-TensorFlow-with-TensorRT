# Build-TensorFlow-with-TensorRT

This repository contains helper Dockerfiles and build scripts to produce TensorFlow python wheels built **with NVIDIA TensorRT** support for specific Python, CUDA, and cuDNN combinations. 

This project was born out of the work I did in trying to get convert keras models to TensorRT models on an HPC running Rocky Linux 9. (hence why the docker images are all Rocky Linux 9). I initially went with Ubuntu images, but the wheels they produced were not compatible with the GLIBC runtime of the HPC. This HPC system is the only system I have tested this project with, so it may well be that they don't work for some other systems. Smilarly, there is no ARM support, although NVIDIA Ubuntu arm64 containers do exist, so it shouldn't be too hard to add support for ARM (e.g. the Jetson).

**This is not feature complete nor intended to be.** Contributions are welcome. ***You are on your own trying to fix issues.*** Considering that I fixed most of mine with ChatGPT, it's not too hard. 

The TensorRT I opted to use is the latest offered by NVIDIA that is still compatible with TensorFlow ([Version 8.6.1](https://developer.nvidia.com/nvidia-tensorrt-8x-download))

**Prerequisites**
- Linux host with recent Docker installed (no GPU is needed to build)
- Sufficient disk space and memory for building TensorFlow (tens of GBs Disk Space, 16 GB of RAM at least)
- Lots of time!!!! (4-8 hours)

**Usage**

1) Choose the configuration directory that matches the TensorFlow/Python/CUDA/cuDNN/ combination you want. Example:
```
cd 2.16.2/tf-cuda12.1-cudnn8.9-TRT-8.6.1/
```
2) Build the docker image:
```
docker build -t build_TF -f Dockerfile .
```
3) Enter the docker image:
```
docker run --rm -it build_TF /bin/bash
```
4) Start the TensorFlow build:
```
./build_tf.sh
```
The `build_tf.sh` script executes inside the docker image to build TensorFlow. Edit this if you want to change something about the build configuration. You will need to rebuild the docker image if you make changes.

5) Export the built wheel:
```
docker cp build_TF:/output ./
```
6) Check the wheel:
```
pip install <your built wheel file>
import tensorflow as tf
print(tf.__version__)
print(tf.sysconfig.get_build_info())
print(tf.config.list_physical_devices('GPU'))
```

**Customization**
- To change build flags or additional dependencies, edit the `Dockerfile` and `build_tf.sh` in the chosen directory.
- Add or change Bazel flags in the build steps to tune performance or enable/disable features.

**Troubleshooting**

- If Docker build fails with CUDA or driver errors, ensure your host NVIDIA driver is compatible with the CUDA runtime used by the image.
- Out-of-memory errors: increase Docker build resources or swap; building TensorFlow can be memory intensive.
- If TensorRT symbols are missing at runtime (`TF-TRT Warning: Could not find TensorRT`), run `python test-tf.py` and check your CUDA and cuDNN versions. If they aren't found, then install them. If you see any 'not found' errors in loading .so libraries, make sure you have them in your `$LD_LIBRARY_PATH`. 
- *Unlike* running `pip install tensorflow[and-cuda]`, which bundles CUDA and cuDNN internally, these wheels *do not include CUDA or cuDNN libraries*, and **those must be installed from NVIDIA.** (This is often already the case with CUDA, but you may be missing cuDNN libraries)
- It goes without saying that you also have to download TensorRT libraries as well. Make sure they are the same as the ones you built TensorFlow against. They must be in your `$LD_LIBRARY_PATH`.

**Contributing configurations**

- Add a new folder following the existing naming pattern for additional Python/TF/CUDA/cuDNN/TRT combinations and include a `Dockerfile` and `build_tf.sh`.


