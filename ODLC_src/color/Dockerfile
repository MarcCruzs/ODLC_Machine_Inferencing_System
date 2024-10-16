FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /usr/app/src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

ENTRYPOINT [ "./src/entrypoint.sh" ]