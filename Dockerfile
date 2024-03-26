#defining the pre defined image for python from hub.docker.com
FROM python:3.9-alpine3.13 
LABEL maintainer="sayyam44"

#this directly gives the output of the python without any buffer
ENV PYTHONUNBUFFERED 1 

#copies the requirements from local requirements.txt file to the github
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
#workdir is the default direclty where the commandds will run
WORKDIR /app
#expose tells we will expose the port 8000 from our container to the machiune when we run the container
EXPOSE 8000

#this is for below if case 
ARG DEV=false 
#this creates a new virtual env inside docker image that we will use to store our dependencies.
RUN python -m venv /py && \
#to install the python package manajor i.e. pip inside the virtual env
    /py/bin/pip install --upgrade pip && \
    #install postgresql client in alpine imag(basically we are installing the postgresql adpter in docker env)
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    #installing the reqs in virtual env
    /py/bin/pip install -r /tmp/requirements.txt && \
    #the below if case is to use requirements.dev.txt only at development server and not the production sertver
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    #to add a new user inside the image
    adduser \
        --disabled-password \
        --no-create-home \
        django-user 

ENV PATH="/py/bin:$PATH"

USER django-user