FROM python:3.8-alpine3.10

COPY . /app
WORKDIR /app

# update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium

# install packages

RUN pip install modules

EXPOSE 9222
# command
CMD python dataq.py -s 1
#CMD python