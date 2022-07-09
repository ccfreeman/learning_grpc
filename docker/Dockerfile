FROM python:3.9-buster

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# install needed packages
#  assorted Debian packages
#  msodbcsql17
# save space (must be done in the same RUN block to reduce layer size)
#   remove apt cache
# remove unwanted configurations
#   delete cron jobs unrelated to log rotation
# install anaconda requirements
RUN apt-get update --fix-missing \
    && apt-get install -y \
        curl \
        libglib2.0-0\
        libxext6 \
        libsm6 \
        libxrender1 \
        build-essential \ 
        python-lxml \
        unixodbc-dev \
        dos2unix \
    && apt-get clean

RUN curl 'http://pki.coyote.com/trust/zscaler.cer' -o '/usr/local/share/ca-certificates/zscaler.crt'
RUN chmod 644 /usr/local/share/ca-certificates/zscaler.crt && update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

RUN python3 -m pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 PIPENV_NOSPIN=1 pipenv install --deploy

RUN pipenv graph

ENV RUNNING_AS_DOCKER=true
# bring in app logic
COPY ./src /app/src

COPY learning_grpc.config /app/learning_grpc.config
COPY config.py /app/config.py
COPY logging.json /app/logging.json

# # bring in entrypoint script and ensure it's executable
COPY docker/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN dos2unix /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

WORKDIR /app
USER root
EXPOSE 8080
EXPOSE 5056
