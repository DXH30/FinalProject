FROM frolvlad/alpine-gxx

WORKDIR /root

RUN apk add --no-cache make openssh git libpcap-dev

CMD ["/bin/sh"]
