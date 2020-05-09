FROM python:3

LABEL maintainer="Ebonom Mfam ebonom.n.mfam@gmail.com"

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .