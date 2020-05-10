FROM python:3

LABEL maintainer="Ebonom N. Mfam ebonom.n.mfam@gmail.com"

RUN python -m pip install --upgrade pip

COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


CMD python manage.py migrate
CMD gunicorn movies.wsgi:application -w 2