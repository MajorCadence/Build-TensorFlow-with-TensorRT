# Build-TensorFlow-with-TensorRT

This repository contains helper Dockerfiles and build scripts to produce TensorFlow python wheels built **with NVIDIA TensorRT** support for specific Python, CUDA, and cuDNN combinations. The TensorRT I opted to use is the latest offered by NVIDIA that is still compatible with TensorFlow (Version 8.6.1)

Prerequisites
- Linux host with recent Docker installed (no GPU is needed to build)
- Sufficient disk space and memory for building TensorFlow (tens of GBs Disk Space, 16 GB of RAM at least)
- Lots of time!!!! (4-8 hours)

Usage

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

Customization
- To change TF version, build flags, or additional dependencies, edit the `Dockerfile` and `build_tf.sh` in the chosen directory.
- Add or change Bazel flags in the build steps to tune performance or enable/disable features.

Troubleshooting
- If Docker build fails with CUDA or driver errors, ensure your host NVIDIA driver is compatible with the CUDA runtime used by the image.
- Out-of-memory errors: increase Docker build resources or swap; building TensorFlow can be memory intensive.
- If TensorRT symbols are missing at runtime (`TF-TRT Warning: Could not find TensorRT`), run `python test-tf.py` and check your CUDA and cuDNN versions. If they aren't found, then install them. If you see any 'not found' errors in loading .so libraries, make sure you have them in your $PATH.

Contributing configurations
- Add a new folder following the existing naming pattern for additional Python/TF/CUDA/cuDNN/TRT combinations and include a `Dockerfile` and `build_tf.sh`.


