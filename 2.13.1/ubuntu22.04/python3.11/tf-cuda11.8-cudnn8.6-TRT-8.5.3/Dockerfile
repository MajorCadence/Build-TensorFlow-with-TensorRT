FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TF_VERSION=v2.13.1

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    unzip \
    zip \
    software-properties-common \
    pkg-config \
    openjdk-17-jdk \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    xz-utils \
    ca-certificates \
    nano \
    patchelf \
    && rm -rf /var/lib/apt/lists/*


# Install newer GCC (needed for older TF builds)
#RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && apt-get update && apt-get install -y \
#    gcc-11 \
#    g++-11 \
#    && rm -rf /var/lib/apt/lists/*

#ENV CC=/usr/bin/gcc-11
#ENV CXX=/usr/bin/g++-11
#ENV GCC_HOST_COMPILER_PATH=/usr/bin/gcc-11

WORKDIR /tmp

# -------------------------
# Bazel install
# -------------------------


RUN wget https://github.com/bazelbuild/bazel/releases/download/5.3.0/bazel-5.3.0-linux-x86_64 \
     -O /usr/local/bin/bazel && \
     chmod +x /usr/local/bin/bazel

# CUDA

RUN wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run && \
	chmod +x cuda_11.8.0_520.61.05_linux.run && \ 
	sh cuda_11.8.0_520.61.05_linux.run --silent --toolkit && \
	rm cuda_11.8.0_520.61.05_linux.run

# CUDNN

COPY cudnn/cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz /tmp/cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz
RUN tar -xJvf cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz && \
	rm cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz


# -------------------------
# TensorRT
# -------------------------

COPY tensorrt/TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz /tmp/TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz
RUN tar -xzvf TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz && \
	rm TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz

WORKDIR /tensorflow

# TensorFlow

RUN git clone https://github.com/tensorflow/tensorflow.git . && \ 
	git checkout ${TF_VERSION}

# -------------------------
# Python via pyenv
# -------------------------

RUN curl -fsSL https://pyenv.run | bash

ENV HOME="/root"
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN eval "$(pyenv init - bash)" && \
    eval "$(pyenv virtualenv-init -)" && \
    pyenv install 3.11 --verbose && \
    pyenv virtualenv 3.11 tf-build && \
    pyenv global tf-build && \
    pyenv rehash

RUN python -m pip install --upgrade pip setuptools

# Copy scripts over
 
COPY 2.13.1/ubuntu22.04/python3.11/tf-cuda11.8-cudnn8.6-TRT-8.5.3/build_tf.sh /tensorflow/build_tf.sh
COPY check_nvidia_versions.py /tensorflow/check_nvidia_versions.py
RUN chmod +x /tensorflow/check_nvidia_versions.py && chmod +x /tensorflow/build_tf.sh


# -------------------------
# (Optional) Newer binutils
# -------------------------

# WORKDIR /tmp
# RUN wget https://ftp.gnu.org/gnu/binutils/binutils-2.40.tar.xz && \
#     tar -xf binutils-2.40.tar.xz && \
#     mkdir /tmp/binutils-build

# WORKDIR /tmp/binutils-build
# RUN ../binutils-2.40/configure --prefix=/opt/binutils-2.40 && \
#     make -j$(nproc) && \
#     make install

# ENV PATH="/opt/binutils-2.40/bin:${PATH}"

# Go for it!

CMD ./build_tf.sh
