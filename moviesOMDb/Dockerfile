FROM python:3

LABEL maintainer="Ebonom N. Mfam ebonom.n.mfam@gmail.com"

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate
CMD gunicorn movies.wsgi:application -w 2 --bind 0.0.0.0:8000