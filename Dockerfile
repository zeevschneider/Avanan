FROM repo.okro.blue/traiana-docker/github/traiana/base-python37/base-python37:20200812-c55aa098

COPY . /tests
WORKDIR /tests


RUN apt-get update \
    && apt-get --no-install-recommends install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /tests/.venv \
    && . /tests/.venv/bin/activate \
    && pip install -r ./requirements.txt

ENV PROJECT_NAME=Avanan
ENV LOGS_DIR=/tests/tests/logs

ARG proto_version=20200810-e7c74324
RUN mkdir .depo \
    && curl https://repo.okro.blue/artifactory/traiana-files/github/traiana/depo/${proto_version}/python-generated-code.tar.gz -o ".depo/python-generated-code.tar.gz" \
    && tar -xf .depo/python-generated-code.tar.gz --directory .depo \
    && rm .depo/python-generated-code.tar.gz

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["tini", "--"]
CMD ["./docker-entrypoint.sh"]
