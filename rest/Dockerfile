FROM jupyterhub/jupyterhub

ADD . /tmp/build
RUN \
    cd /tmp/build                                  &&  \
    python3 setup.py sdist                         &&  \
    cd dist                                        &&  \
    pip3 install --no-cache-dir rest-0.0.1.tar.gz  &&  \
    cd /tmp                                        &&  \
    rm -rf build
