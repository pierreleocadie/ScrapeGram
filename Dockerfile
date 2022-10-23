FROM python:3.10-buster

RUN mkdir ScrapeGram
COPY ./requirements.txt ScrapeGram/requirements.txt
COPY ./README.md ScrapeGram/README.md
COPY ./src ScrapeGram/src
COPY ./.gitignore ScrapeGram/.gitignore
COPY ./LICENSE ScrapeGram/LICENSE

RUN pip install -r ScrapeGram/requirements.txt