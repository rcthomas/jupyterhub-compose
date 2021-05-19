FROM rest:latest

RUN \
    pip3 install --no-cache-dir \
        aiocache

ADD . /tmp/build
RUN \
    cd /tmp/build                               &&  \
    version=$(python3 setup.py --version)       &&  \
    python3 setup.py sdist                      &&  \
    cd dist                                     &&  \
    pip3 install --no-cache-dir                     \
        images-$version.tar.gz                  &&  \
    cd /tmp                                     &&  \
    rm -rf build

WORKDIR /srv
ADD docker-entrypoint.sh /srv/docker-entrypoint.sh
RUN chmod +x /srv/docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "-u", "-m", "images", "api"]
