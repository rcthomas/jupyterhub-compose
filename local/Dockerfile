FROM ubuntu:latest

WORKDIR /srv

RUN \
    apt-get update          &&  \
    apt-get upgrade --yes   &&  \
    apt-get install --yes       \
        openssh-client

RUN \
    adduser -q --gecos "" --disabled-password admin     && \
    echo admin:admin | chpasswd

RUN \
    adduser -q --gecos "" --disabled-password user1     && \
    echo user1:user1 | chpasswd

ADD test-user.sh .

WORKDIR /srv
ADD docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD ["sleep", "9999"]
