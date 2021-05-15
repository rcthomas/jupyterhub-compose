FROM jupyterhub/jupyterhub

RUN \
    apt-get update          &&  \
    apt-get upgrade --yes   &&  \
    apt-get install --yes       \
        git

RUN \
    pip3 install --no-cache-dir html_sanitizer && \
    pip3 install git+https://github.com/rcthomas/jupyterhub-announcement.git@0.6.0

WORKDIR /srv

ADD docker-entrypoint.sh announcement_config.py ./
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python3", "-m", "jupyterhub_announcement"]
