#!/bin/bash

echo Generating secrets...
rm -rf secrets
mkdir secrets
cd secrets
openssl rand -hex 32 > announcement-api-token.txt
openssl rand -hex 32 > configproxy-auth-token.txt
openssl rand -hex 32 > hub-profiles-token.txt
openssl rand -hex 32 > images-api-token.txt
openssl rand -hex 32 > profile-manager-api-token.txt
openssl rand -hex 32 > profiles-api-token.txt
openssl rand -hex 32 > shifter-api-token.txt
cd ..

echo Generating ssh creds...
ssh-keygen -t rsa -N '' -C ca@localhost -f secrets/creds
ssh-keygen -s secrets/creds -h -I localhost secrets/creds.pub

echo Building announcement...
cd announcement
docker build -t announcement:latest .
cd ..

echo Building hub...
cd hub
docker build -t hub:latest .
cd ..

echo Building rest
cd rest
docker build -t rest:latest .
cd ..

echo Building images
cd images
docker build -t images:latest .
cd ..

echo Building local...
cd local
docker build -t local:latest .
cd ..

echo Building profile-manager...
cd profile-manager
docker build -t profile-manager:latest .
cd ..

echo Building profiles...
cd profiles
docker build -t profiles:latest .
cd ..

echo Building remote...
cd remote
docker build -t remote:latest .
cd ..

echo Building shifter...
cd shifter
docker build -t shifter:latest .
cd ..

