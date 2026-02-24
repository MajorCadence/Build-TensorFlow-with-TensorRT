#!/bin/bash
set -e

echo "Building TensorFlow 2.16.2 with TensorRT for Python 3.10 on Rocky 9..."

pip install -r requirements_lock_3_10.txt

export PYTHON_BIN_PATH=/root/.pyenv/versions/tf-build/bin/python3
export PYTHON_LIB_PATH=/root/.pyenv/versions/tf-build/lib/python3.10/site-packages
export TF_ENABLE_XLA=1
export TF_NEED_CUDA=1
export TF_NEED_TENSORRT=1
export TF_CUDA_VERSION=12.1
export TF_CUDNN_VERSION=8.9
export TF_TENSORRT_VERSION=8.6
export TF_CUDA_COMPUTE_CAPABILITIES=8.6
export CUDA_TOOLKIT_PATH=/usr/local/cuda
export CUDNN_INSTALL_PATH=/usr
export TENSORRT_INSTALL_PATH=/tmp/TensorRT-8.6.1.6
export TF_NEED_ROCM=0
export TF_NEED_MPI=0
export TF_NEED_OPENCL=0
export TF_CUDA_CLANG=0
export TF_SET_ANDROID_WORKSPACE=0
export TF_PYTHON_VERSION=3.10
export GCC_HOST_COMPILER_PATH=/usr/bin/gcc
export CC_OPT_FLAGS=-Wno-sign-compare

./configure

#bazel clean --expunge

bazel build \
  --config=cuda \
  --config=tensorrt \
  --repo_env=TF_CUDA_COMPUTE_CAPABILITIES=8.6 \
  --copt=-march=native \
  //tensorflow/tools/pip_package:build_pip_package

./bazel-bin/tensorflow/tools/pip_package/build_pip_package /output

echo "Build complete."
