#!/bin/bash

for u in $(ls /home/); do
    cp /run/secrets/creds /tmp/$u.key
    chmod 600 /tmp/$u.key
    cp /run/secrets/creds-cert.pub /tmp/$u.key-cert.pub
    chmod 600 /tmp/$u.key-cert.pub
done

exec "$@"
