#!/bin/usr

pip install --user virtualenv

mkdir venv

python -m virtualenv venv

source venv/bin/activate.csh

pip install nltk

python -m nltk.downloader all

pip install spacy

python -m spacy download en
