#!/bin/sh

imageTag="lennybontenakel/tika-text-extractor:latest"
docker build -t ${imageTag} . && docker push ${imageTag}
