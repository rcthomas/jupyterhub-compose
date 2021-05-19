FROM jupyterhub/jupyterhub

WORKDIR /srv
ADD admin /srv/list/admin
ADD user1 /srv/list/user1
CMD ["python3", "-m", "http.server"]
