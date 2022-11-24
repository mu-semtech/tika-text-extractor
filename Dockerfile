FROM semtech/mu-python-template:2.0.0-beta.1
LABEL maintainer="lennyb.0908@gmail.com"

# Install Java 11 for Tika
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean; 

ENV PYTHONIOENCODING="utf8"
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ENV TIKA_SERVER_JAR=file:///app/tika-server/tika-server-1.24.jar
ENV LOGLEVEL=WARNING

