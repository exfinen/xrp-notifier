#!/bin/bash

if [ -e lambda.zip ]; then
  rm -f lambda.zip
  echo 'deleted lambda.zip'
fi

mkdir lambda
if [ -d lambda ]; then
  rm -rf lambda
fi
mkdir lambda

pushd lambda
cp ../xrp_notifier.py .
cp ../requirements.txt .
pip install -r ./requirements.txt -t .
popd

zip -r lambda.zip lambda

rm -rf lambda

