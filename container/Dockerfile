FROM ubuntu:18.04

# update apt and get miniconda
RUN apt-get update \
    && apt-get install -y wget \
    && apt-get install -y git 


ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Install Miniconda on x86 or ARM platforms
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"; \
    elif [ "$arch" = "aarch64" ]; then \
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"; \
    else \
    echo "Unsupported architecture: $arch"; \
    exit 1; \
    fi && \
    wget $MINICONDA_URL -O miniconda.sh && \
    mkdir -p /root/.conda && \
    bash miniconda.sh -b -p /root/miniconda3 && \
    rm -f miniconda.sh

RUN git clone https://github.com/lsst/rubin_scheduler.git 

# install rubin_scheduler
RUN cd rubin_scheduler \
    && conda init bash \
    && . ~/.bashrc \
    && conda create --channel conda-forge --name rubin --file requirements.txt python=3.11 \
    && conda activate rubin \
    && pip install -e . --no-deps

RUN cd rubin_scheduler/tests/scheduler \
    && conda init bash \
    && . ~/.bashrc \
    && conda activate rubin \
    && python test_nside.py


