FROM frolvlad/alpine-gxx

WORKDIR /root

RUN apk add --no-cache make openssh git 
COPY . /root/FinalProject

RUN ls -la

RUN cd /root/FinalProject; git pull

CMD ["/bin/sh"]
