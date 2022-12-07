#! /usr/bin/env sh

mkdir /logs
started=false

while [ "$started" = false ]
do
	{ 
		echo "Attempting connect" >> /logs/startup.txt
		curl -X POST http://127.0.0.1/index-all	
	} || {
		sleep 3
		echo "Retrying" >> /logs/startup.txt
		continue
	}
	echo "Server started" >> /logs/startup.txt
	started=true
done

echo "Process finished" >> /logs/startup.txt
