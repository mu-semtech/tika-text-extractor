FROM lennybontenakel/custom-python-template:latest
LABEL maintainer="lennyb.0908@gmail.com"

# Overrides the start.sh used in `semtech/mu-python-template`
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

RUN chmod +x /app/ping-server.sh

# Install Java 11 for Tika
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean; 

ENV PYTHONIOENCODING="utf8"
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ENV TIKA_SERVER_JAR=file:///app/tika-server/tika-server-1.24.jar
