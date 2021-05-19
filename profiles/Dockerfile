FROM rest:latest

RUN \
    pip3 install --no-cache-dir \
        motor

ADD . /tmp/build
RUN \
    cd /tmp/build                   &&  \
    python3 setup.py sdist          &&  \
    cd dist                         &&  \
    pip3 install --no-cache-dir         \
        profiles-0.0.1.tar.gz       &&  \
    cd /tmp                         &&  \
    rm -rf build

WORKDIR /srv
ADD docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod +x /srv/docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "-u", "-m", "profiles", "file"]
