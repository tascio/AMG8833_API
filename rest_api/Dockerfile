FROM python:3.10

COPY requirements.txt /app/requirements.txt
COPY ./app /app
RUN pip install -r /app/requirements.txt

WORKDIR /app

#CMD ["python", "app.py"]
#CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5050", "app:app", "--log-level=info", "--access-logfile=-", "--error-logfile=-"]