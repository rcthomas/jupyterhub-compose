FROM jupyterhub/jupyterhub

RUN \
    python3 -m pip install --no-cache jupyterlab

RUN \
    adduser -q --gecos "" --disabled-password admin     && \
    echo admin:admin | chpasswd

RUN \
    adduser -q --gecos "" --disabled-password user1     && \
    echo user1:user1 | chpasswd

ADD templates templates

ADD docker-entrypoint.sh docker-entrypoint.sh
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["jupyterhub"]
