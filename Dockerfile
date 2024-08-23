FROM python:3.9-slim

WORKDIR /app/

COPY app.py /app/
COPY utils /app/utils
COPY tests /app/tests
COPY templates  /app/templates
COPY static /app/static
COPY requirements.txt /app/
COPY google_services /app/google_services
COPY database /app/database


RUN pip install --no-cache-dir -r /app/requirements.txt


ARG SENDINBLU_API_KEY

ENV GOOGLE_API_CREDENTIALS=/app/google_services/credentials.json


EXPOSE 5000

CMD ["python", "app.py"]