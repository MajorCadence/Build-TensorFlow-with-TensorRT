FROM nvidia/cuda:11.8.0-cudnn8-devel-rockylinux8

ENV TF_VERSION=v2.14.0


RUN dnf -y groupinstall "Development Tools" && \
	dnf install -y dnf-plugins-core && dnf config-manager --set-enabled powertools && dnf install -y texinfo wget && \
    dnf -y install \
        java-17-openjdk-devel \
        openssl-devel \
        which \
        libxcrypt \
        nano \
        bzip2-devel \
        readline-devel \
        sqlite \
        sqlite-devel \
        openssl-devel \
        tk-devel \
        libffi-devel \
        gcc-toolset-11 && \
    dnf clean all


RUN wget https://github.com/bazelbuild/bazel/releases/download/6.1.0/bazel-6.1.0-linux-x86_64 \
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
RUN wget "https://developer.download.nvidia.com/compute/machine-learning/tensorrt/secure/8.5.3/tars/TensorRT-8.5.3.1.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz?__token__=exp=1774886359~hmac=fe2160949143b8625a17f401de542507b2af1f998c18cc40988070d995cd57e7&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9" && \
	tar -xzf TensorRT-8.5.3.*

RUN git clone https://github.com/NixOS/patchelf.git
WORKDIR /tmp/patchelf
RUN ./bootstrap.sh && ./configure && make && make install
WORKDIR /tmp
RUN wget https://ftp.gnu.org/gnu/binutils/binutils-2.40.tar.xz && \
	tar -xf binutils-2.40.tar.xz && mkdir /tmp/binutils-build
WORKDIR /tmp/binutils-build
RUN ../binutils-2.40/configure --prefix=/opt/binutils-2.40 && make -j$(nproc) && make install

ENV PATH="/opt/binutils-2.40/bin:${PATH}"
WORKDIR /tensorflow

COPY build_tf.sh /tensorflow/build_tf.sh
RUN chmod +x /tensorflow/build_tf.sh
