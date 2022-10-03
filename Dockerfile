FROM semtech/mu-python-template:2.0.0-beta.1
LABEL maintainer="lennyb.0908@gmail.com"

ENV LOGLEVEL="DEBUG"
ENV PYTHONIOENCODING="utf8"


# Install Java 11 for Tika
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean; 

# ENV TIKA_SERVER_JAR="file:////tmp/tika-server-1-9.jar" 
