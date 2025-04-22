FROM python:3.10

COPY requirements.txt /app/requirements.txt
COPY ./app /app
RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "-u", "app.py"]