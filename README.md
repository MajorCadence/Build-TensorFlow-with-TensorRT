# Build-TensorFlow-with-TensorRT

This repository contains helper Dockerfiles and build scripts to produce TensorFlow binaries built with NVIDIA TensorRT support for specific CUDA and cuDNN combinations.

Prerequisites
- Linux host with recent Docker installed (no GPU is needed to build)
- Sufficient disk space and memory for building TensorFlow (tens of GBs Disk Space, 16 GB of RAM at least)
- Lots of time!!!! (4-8 hours)

Usage

1) Choose the configuration directory that matches the CUDA/cuDNN/TFRT combination you want. Example:

```
cd tf-cuda12.4-cudnn9.1-TRT-8.6.1
```

2) Build the image:

```
docker build -t tf-trt:cuda12.4 -f Dockerfile .
```
The `build_tf.sh` script executes inside the docker image to build TensorFlow. Edit this if you want to change something about the configuration.

3) Export the built wheel:

```
docker cp tf-trt:cuda12.4:/output ./
```

```
python -c "import tensorflow as tf; print(tf.__version__); print('CUDA:', tf.test.is_built_with_cuda()); print('GPU count:', len(tf.config.list_physical_devices('GPU')))")
```

Customization
- To change TF version, build flags, or additional dependencies, edit the `Dockerfile` and `build_tf.sh` in the chosen directory.
- Add or change Bazel flags in the build steps to tune performance or enable/disable features.

Troubleshooting
- If Docker build fails with CUDA or driver errors, ensure your host NVIDIA driver is compatible with the CUDA runtime used by the image.
- Out-of-memory errors: increase Docker build resources or swap; building TensorFlow can be memory intensive.
- If TensorRT symbols are missing at runtime, verify that your runtime environment has the same TensorRT version as used during linking.

Contributing
- Add a new folder following the existing naming pattern for additional CUDA/cuDNN/TRT combinations and include a `Dockerfile` and `build_tf.sh`.


