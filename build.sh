#!/bin/bash

echo Generating secrets...
rm -rf secrets
mkdir secrets
cd secrets
openssl rand -hex 32 > announcement-api-token.txt
openssl rand -hex 32 > configproxy-auth-token.txt
cd ..

echo Building hub...
cd hub
docker build -t hub:latest .
cd ..

echo Building announcement...
cd announcement
docker build -t announcement:latest .
cd ..
