# Multistage docker build, requires docker 17.05

# builder stagedevel
FROM intel/intel-gpu-plugin:devel as builder

RUN set -ex && \
    apt-get update && \
    apt-get --no-install-recommends --yes install \
        build-essential \
        git libssl-dev \
        libpcre3-dev \
        apt-transport-https \
        ca-certificates \
        libcurl4-openssl-dev && \
    # git clone https://github.com/exploitagency/vanitygen-plus && \
    # cd vanitygen-plus && \
    # make all

COPY . /vanitygen-master

RUN cd vanitygen-master && \
    make all
# runtime stage
FROM intel/intel-gpu-plugin:devel

RUN set -ex && \
    apt-get update && \
    apt-get --no-install-recommends --yes install libssl1.0.0 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /vanitygen-master /vanitygen-master

WORKDIR /vanitygen-master
ENTRYPOINT ["./oclvanitygen"]
