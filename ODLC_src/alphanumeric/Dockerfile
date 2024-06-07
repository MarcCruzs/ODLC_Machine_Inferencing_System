#Dockerfile, Image, Container
FROM python:3.8

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /usr/app/src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

RUN chmod +x ./src/entrypoint.sh

ENTRYPOINT [ "./src/entrypoint.sh" ]

