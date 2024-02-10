FROM python:3.10.8-slim-buster

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "-m", "gunicorn", "run:app"]
