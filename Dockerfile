FROM python:3.10.8-slim-buster

RUN pip install --upgrade pip

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_ENV production

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "run:app"]
