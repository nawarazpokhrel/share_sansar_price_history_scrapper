FROM python:3.8 
ENV DockerHOME=/home/app/nepsealpa  

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN apt update && apt install gettext -y
RUN apt install poppler-utils -y
RUN pip install --upgrade pip  
RUN pip install celery[redis]
COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . $DockerHOME 
ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
