FROM python:3.10.8-slim-buster

RUN pip install --upgrade pip

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_ENV production
ENV WEB_HOST 0.0.0.0
ENV WEB_PORT 8000

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE $WEB_PORT

CMD ["python", "-m", "gunicorn", "run:app"]
