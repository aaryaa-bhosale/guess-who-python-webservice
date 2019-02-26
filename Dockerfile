FROM ubuntu:16.04

MAINTAINER Your Name "aaryaa.bhosale@infobeans.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /python_guesswho_api

RUN pip3 install -r requirements.txt

COPY . /python_guesswho_api

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

