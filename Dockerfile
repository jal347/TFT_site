# syntax=docker/dockerfile:1
FROM ubuntu
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get install -y python3-pip
RUN pip3 install pymongo
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install requests
RUN pip3 install matplotlib
COPY . /code
WORKDIR /code

EXPOSE 5000


ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]