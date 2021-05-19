FROM jupyterhub/jupyterhub

RUN \
    apt-get update          &&  \
    apt-get install --yes       \
        git

RUN \
    pip3 install --no-cache-dir \
        git+https://github.com/rcthomas/jupyterhub-service-page

ADD . /tmp/build
RUN \
    cd /tmp/build                       &&  \
    python3 setup.py sdist              &&  \
    cd dist                             &&  \
    pip3 install --no-cache-dir             \
        profile-manager-0.0.1.tar.gz    &&  \
    cd /tmp                             &&  \
    rm -rf build

WORKDIR /srv
ADD page_config.py /srv/page_config.py
ADD templates /srv/templates

ADD docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "-u", "-m", "profile_manager", "--Service.config_file=page_config.py"]
