#Dockerfile, Image, Container
FROM python:3.8

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app

ADD main.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

ENTRYPOINT ["python", "/app/main.py"]

