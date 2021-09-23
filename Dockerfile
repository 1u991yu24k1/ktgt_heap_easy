FROM phusion/baseimage:master-amd64
#MAINTAINER skysider <skysider@163.com>

ENV DEBIAN_FRONTEND noninteractive

ENV TZ Asia/Tokyo

RUN dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt install -y \
    libc6-dbg \
    g++-multilib \
    cmake \
    python3 \
    vim \
    net-tools \
    iputils-ping \
    libffi-dev \
    libssl-dev \
    python3-dev \
    python3-pip \
    build-essential \
    ruby \
    ruby-dev \
    strace \
    ltrace \
    nasm \
    wget \
    gdb \
    netcat \
    socat \
    git \
    patchelf \
    gawk \
    file \
    python3-distutils \
    bison \
    cpio \
    zstd \
    tzdata --fix-missing && \
    rm -rf /var/lib/apt/list/*

RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
    
RUN python3 -m pip install -U pip && \
    python3 -m pip install --no-cache-dir \
    pwntools \
    z3-solver \
    ropper \
    unicorn \
    keystone-engine \
    capstone \
    angr \
    hexdump 


RUN gem install one_gadget seccomp-tools && rm -rf /var/lib/gems/2.*/cache/*

RUN wget -q https://raw.githubusercontent.com/bata24/gef/dev/install.sh -O- | sh

WORKDIR /ctf/work/

#COPY --from=skysider/glibc_builder64:2.23 /glibc/2.23/64 /glibc/2.23/64
COPY --from=skysider/glibc_builder64:2.27 /glibc/2.27/64 /glibc/2.27/64
COPY --from=skysider/glibc_builder64:2.31 /glibc/2.31/64 /glibc/2.31/64
RUN mkdir -p /glibc/src && git clone git://sourceware.org/git/glibc.git /glibc/src

CMD ["/sbin/my_init"]
