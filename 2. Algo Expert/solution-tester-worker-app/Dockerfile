FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN mkdir /tmp-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003"]
