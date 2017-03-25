FROM ubuntu:14.04

MAINTAINER robin robin890650@gmail.com

RUN apt-get update && \
    apt-get dist-upgrade -y --force-yes && \
    apt-get install python-pip -y --force-yes

RUN pip install django facepy && \
    apt-get install python-pandas -y --force-yes

ENV VERSION=0
WORKDIR /opt
RUN apt-get install git -y --force-yes && \
    git clone https://github.com/JiaMingLin/facebook_like.git

ADD start.sh /opt/facebook_like/start.sh
RUN chmod +x /opt/facebook_like/start.sh

VOLUME ["/opt/facebook_like/"] 

WORKDIR /opt/facebook_like
EXPOSE 8080
ENTRYPOINT /opt/facebook_like/start.sh
