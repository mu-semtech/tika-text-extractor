FROM semtech/mu-python-template:2.0.0-beta.1
LABEL maintainer="lennyb.0908@gmail.com"


ENV FILE_RESOURCE_BASE=http://mu.semte.ch/services/file-service/files/
ENV MU_APPLICATION_FILE_STORAGE_PATH=files/toExtract/
ENV MU_SPARQL_ENDPOINT=http://database:8890/sparql
ENV MU_SPARQL_TIMEOUT=60
ENV LOG_LEVEL=info