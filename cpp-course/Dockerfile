FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

COPY install_deps.sh /

RUN sh install_deps.sh

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN echo "StrictHostKeyChecking=no" >> /etc/ssh/ssh_config
EXPOSE 22

# User for CLion
RUN groupadd -g 712342 clion_user_group
RUN useradd -u 712342 -g 712342 -m clion_user && yes password | passwd clion_user

RUN mkdir /var/run/sshd

ENV CXX="/usr/bin/clang++-10"
ENV CC="/usr/bin/clang-10"

CMD ["/usr/sbin/sshd", "-D"]

