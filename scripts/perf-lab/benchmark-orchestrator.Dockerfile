FROM registry.access.redhat.com/ubi9/ubi
LABEL org.opencontainers.image.source="https://github.com/quarkusio/spring-quarkus-perf-comparison"

USER root

# Install system dependencies, container runtime, and Java 21
# Java installed via dnf so both amd64 and arm64 get native packages —
# prevents JBang from downloading its own JDK (which fails on arm64).
RUN dnf install -y --allowerasing gcc zlib-devel git procps-ng curl file bash unzip zip sudo podman fuse-overlayfs slirp4netns shadow-utils java-21-openjdk-devel

# Set up subuid and subgid for rootless containers BEFORE creating user
RUN touch /etc/subuid /etc/subgid && \
    chmod 644 /etc/subuid /etc/subgid && \
    echo "benchmark:100000:65536" >> /etc/subuid && \
    echo "benchmark:100000:65536" >> /etc/subgid

# Add a new non-root user
RUN useradd -u 1000 -g wheel -s /bin/bash benchmark

# Allow benchmark user to use sudo without password
RUN echo "benchmark ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/benchmark && \
    chmod 0440 /etc/sudoers.d/benchmark

# Install homebrew
# RUN curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash

USER benchmark
WORKDIR /home/benchmark

# Install nvm
RUN touch ~/.bashrc && chmod +x ~/.bashrc
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
RUN . ~/.nvm/nvm.sh && \
    nvm install --lts && \
    nvm use --lts

# Install SDKMAN, then use it to install JBang
# SDKMAN handles arm64 natively; no separate JDK download needed (system Java 21 is used)
RUN curl -s "https://get.sdkman.io" | bash
RUN bash -c "source ~/.sdkman/bin/sdkman-init.sh && sdk install jbang"

# Configure homebrew
# ENV HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew \
# 	HOMEBREW_CELLAR=/home/linuxbrew/.linuxbrew/Cellar \
# 	HOMEBREW_REPOSITORY=/home/linuxbrew/.linuxbrew/Homebrew \
# 	PATH=/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}
#
#RUN	echo "eval \$(${HOMEBREW_PREFIX}/bin/brew shellenv)" >> ~/.bashrc

# Keep container running and wait for connections
CMD ["tail", "-f", "/dev/null"]
