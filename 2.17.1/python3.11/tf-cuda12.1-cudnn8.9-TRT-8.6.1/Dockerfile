FROM nvidia/cuda:12.1.1-cudnn8-devel-rockylinux9

ENV TF_VERSION=v2.17.1


RUN dnf -y groupinstall "Development Tools" && \
	dnf install -y dnf-plugins-core && dnf config-manager --set-enabled crb && dnf install -y texinfo wget && \
    dnf -y install \
        git \
        wget \
        unzip \
        zip \
        java-17-openjdk-devel \
        openssl-devel \
        which \
        libxcrypt-compat \
        nano \
        gcc \
        make \
        patch \
        zlib-devel \
        bzip2 \
        bzip2-devel \
        readline-devel \
        sqlite \
        sqlite-devel \
        openssl-devel \
        tk-devel \
        libffi-devel \
        xz-devel \ 
        gcc-toolset-12 \
        gcc-toolset-12-gcc \
        gcc-toolset-12-gcc-c++ && \
    dnf clean all


RUN wget https://github.com/bazelbuild/bazel/releases/download/6.5.0/bazel-6.5.0-linux-x86_64 \
    -O /usr/local/bin/bazel && \
    chmod +x /usr/local/bin/bazel


WORKDIR /tensorflow
RUN git clone https://github.com/tensorflow/tensorflow.git . && \
    git checkout ${TF_VERSION}


WORKDIR /root

RUN curl -fsSL https://pyenv.run | bash
ENV HOME="/root"
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
RUN eval "$(pyenv init - bash)" && eval "$(pyenv virtualenv-init -)" && pyenv install 3.11 --verbose && pyenv virtualenv 3.11 tf-build && pyenv global tf-build && pyenv rehash
RUN python -m pip install --upgrade pip setuptools wheel numpy

WORKDIR /tmp
RUN wget https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/secure/8.6.1/tars/TensorRT-8.6.1.6.Linux.x86_64-gnu.cuda-12.0.tar.gz && \
	tar -xzf TensorRT-8.6.1.*.tar.gz

RUN git clone https://github.com/NixOS/patchelf.git
WORKDIR /tmp/patchelf
RUN ./bootstrap.sh && ./configure && make && make install && ln -s /usr/local/bin/patchelf /usr/bin/patchelf
WORKDIR /tmp
RUN wget https://ftp.gnu.org/gnu/binutils/binutils-2.40.tar.xz && \
	tar -xf binutils-2.40.tar.xz && mkdir /tmp/binutils-build
WORKDIR /tmp/binutils-build
RUN ../binutils-2.40/configure --prefix=/opt/binutils-2.40 && make -j$(nproc) && make install

ENV PATH="/opt/binutils-2.40/bin:${PATH}"
WORKDIR /tensorflow

COPY build_tf.sh /tensorflow/build_tf.sh
RUN chmod +x /tensorflow/build_tf.sh
